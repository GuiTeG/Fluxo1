import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# Fullscreen automático
fullscreen_script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(() => {
        const elem = document.documentElement;
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
    }, 1000);
});
</script>
"""
components.html(fullscreen_script, height=0, width=0)

# Título
st.title("Dashboard de Vendas")

# Dados
meses = ['Março', 'Fevereiro', 'Janeiro', 'Dezembro', 'Novembro', 'Outubro',
         'Setembro', 'Agosto', 'Julho', 'Junho', 'Maio', 'Abril']
vendas_atual = [7811808, 10557261, 10292922, 9851184, 9945762, 11574936,
                10173150, 9322953, 9506321, 10134793, 9676588, 9410128]
vendas_anterior = [9269070, 9664691, 8922073, 9764371, 9786126, 11385105,
                   9895003, 9174218, 9263091, 10033269, 9483645, 9362865]

hovertext_atual = [f'Mês: {m}<br>Vendas Ano Atual: R$ {v:,.2f}' for m, v in zip(meses, vendas_atual)]
hovertext_anterior = [f'Mês: {m}<br>Vendas Ano Anterior: R$ {v:,.2f}' for m, v in zip(meses, vendas_anterior)]

# Gráfico
fig = go.Figure()
fig.add_trace(go.Bar(
    x=meses,
    y=vendas_atual,
    name='Ano Atual',
    marker_color='#F1B19D',
    text=[f'R$ {v:,.2f}' for v in vendas_atual],
    textposition='inside',
    textfont=dict(color='black', size=12),
    hovertext=hovertext_atual,
    hoverinfo='text'
))
fig.add_trace(go.Bar(
    x=meses,
    y=vendas_anterior,
    name='Ano Anterior',
    marker_color='#E9633A',
    text=[f'R$ {v:,.2f}' for v in vendas_anterior],
    textposition='inside',
    textfont=dict(color='black', size=12),
    hovertext=hovertext_anterior,
    hoverinfo='text'
))
fig.update_layout(
    title='Comparativo de Vendas Mês a Mês',
    xaxis_title='Meses',
    yaxis_title='Vendas',
    yaxis_tickformat='R$,.2f',
    barmode='group',
    legend=dict(x=1, y=1),
    template='plotly',
    font=dict(color='black')
)

# Mostrar gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)
