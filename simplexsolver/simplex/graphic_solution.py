import numpy as np
import plotly.graph_objects as go
import math

def update_restrictions(A, b):
    res = np.hstack((A, np.expand_dims(b, axis=1)))
    return res


def create_convex_area(x, y, X, Y, res, constraints, fig):
    """ Cria a área convexa a partir das restrições """
    Z = np.zeros(X.shape)
    for i, constraint in enumerate(constraints):
        if constraint == "<=":
            Z += (res[i, 0] * X + res[i, 1] * Y <= res[i, 2])
        elif constraint == ">=":
            Z += (res[i, 0] * X + res[i, 1] * Y >= res[i, 2])

    min_x = X >= 0
    min_y = Y >= 0

    Z += min_x
    Z += min_y

    fig.add_trace(go.Contour(x=x, y=y, z=Z, showscale=False, colorscale="bupu",
                  hovertemplate='x₁: %{x}<br>x₂: %{y}<extra></extra> <br>', contours=dict(showlines=True)))

    return Z


def create_lines(fig, x, y, res, constraints):
    """ Cria as linhas das restrições """
    for i in range(res.shape[0]):
        if res[i, 1] != 0:
            m = -res[i, 0] / res[i, 1]
            b = res[i, 2] / res[i, 1]
            fig.add_trace(go.Scatter(x=x, y=m*x + b, mode='lines', line=dict(color='#E3170A'),
                          name=f'{res[i][0]}x₁ + {res[i][1]}x₂ {constraints[i]} {res[i][2]}'))
        else:
            fig.add_shape(type="line", x0=res[i, 2], x1=res[i, 2], y0=y.min(), y1=y.max(), line=dict(
                color="#E3170A"), name=f'{res[i][0]}x₁ + {res[i][1]}x₂ {constraints[i]} {res[i][2]}', showlegend=True)

    fig.add_shape(type="line", x0=x.min(), x1=x.max(),
                  y0=0, y1=0, line=dict(color="black"))
    fig.add_shape(type="line", x0=0, x1=0, y0=y.min(),
                  y1=y.max(), line=dict(color="black"))


def create_level_set(c, fig, x, variables):
    """Definição da Curva de Nível"""
    m = -c[0] / c[1]
    b = c[1]
    
    slider_trace_indices = []
    for step in np.arange(0, variables[0] + 4, 0.1):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color='#F59B00', dash="dot", width=4),
                name= "Curva de Nível",
                x = x,
                y = m*x + b + step  
            )
        )        
        slider_trace_indices.append(len(fig.data) - 1)
    
    steps = []
    for _ , trace_index in enumerate(slider_trace_indices):
        visible = [fig.data[j].visible for j in range(len(fig.data))] 
        visible = [False if j in slider_trace_indices else visible[j] for j in range(len(fig.data))]  
        visible[trace_index] = True  
        step = dict(
            method="update",
            args=[{"visible": visible}],
            label="")
        steps.append(step)
    
    sliders = [dict(
        active=0,
        currentvalue={"prefix": f""},
        pad={"t": 50},
        steps=steps,
        ticklen=0,
    )]

    return sliders


def create_op(variables, int_variables, fig, c):
    """ Definição dos pontos ótimos """
    fig.add_trace(go.Scatter(x=[variables[0]], y=[variables[1]], mode='markers', name=f'Z ∈ ℝ = {round(c[0] * variables[0] + c[1] * variables[1], 2)}', marker=dict(color="#A2C5AC", size=10, line=dict(
        color='black',
        width=2
    ))))
    fig.add_trace(go.Scatter(x=[int_variables[0]], y=[int_variables[1]], mode='markers', name=f'Z ∈ ℤ = {round(c[0] * int_variables[0] + c[1] * int_variables[1], 2)}', marker=dict(color="#ffa8a8", size=10, line=dict(
        color='black',
        width=2
    ))))


def get_int_solution(solution, A, b, c, constraints, problem_type):
    """Função que  arredonda os pontos contínuos do gráfico solução para variáveis inteiras"""
    
    int_points = [[math.floor(solution[0]), math.floor(solution[1])],
                  [math.floor(solution[0]), math.ceil(solution[1])],
                  [math.ceil(solution[0]), math.floor(solution[1])],
                  [math.ceil(solution[0]), math.ceil(solution[1])]]
    
    if problem_type == "max":
        best_z = -math.inf
    elif problem_type == "min":
        best_z = math.inf

    for point in int_points:
        if is_feasible(point, A, b, constraints):
            z_int = sum(point[i] * coef for i, coef in enumerate(c[:2]))
            if problem_type == "max" and z_int > best_z:
                best_z = z_int
                best_point = point
            if problem_type == "min" and z_int < best_z:
                best_z = z_int
                best_point = point
    return best_point


def is_feasible(point, A, b, constraints):
    """" Verifica se a solução encontrada não fere as restrições do problema """
    
    for i in range(len(A)):
        """Calcula o valor do "lado esquerdo" a partir do produto escalar"""
        
        lhs = np.dot(A[i], point)
        
        # Checa se alguma condiçâo não é satisfeita
        if constraints[i] == "<=" and lhs > b[i]:
            return False
        elif constraints[i] == ">=" and lhs < b[i]:
            return False
        elif constraints[i] == "=" and lhs != b[i]:
            return False

    # Se todas as condições forem satisfeitas retorna True
    return True


def create_graph(A, b, c, constraints, variables, problem_type):
    res = update_restrictions(A, b)

    x = np.linspace(0, variables[0] + 5, 400)
    y = np.linspace(0, variables[1] + 5, 400)
    X, Y = np.meshgrid(x, y)

    fig = go.Figure()
    fig.add_shape(type="line", x0=x.min(), x1=x.max(),
                  y0=0, y1=0, line=dict(color="black"))
    fig.add_shape(type="line", x0=0, x1=0, y0=y.min(),
                  y1=y.max(), line=dict(color="black"))
    create_lines(fig, x, y, res, constraints)

    if "=" not in constraints:
        create_convex_area(x, y, X, Y, res, constraints, fig)

    fig.update_xaxes(range=[-1, np.max(x)])
    fig.update_yaxes(range=[-1, np.max(y)])

    sliders = create_level_set(c, fig, x, variables)

    int_variables = get_int_solution(variables, A, b, c, constraints, problem_type)

    create_op(variables, int_variables, fig, c)

    fig.update_layout(
        sliders=sliders,
        plot_bgcolor='white',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        autosize=False,
        width=600,
        height=600,
        title='Gráfico de Intersecções',
        xaxis_title="x₁",
        yaxis_title="x₂",
        font=dict(
            family="Roboto Mono, sans-serif",
            size=16,
            color="#7f7f7f"
        ),
    )
    
    return fig.to_html(full_html=False)

