import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Configuração da página
st.set_page_config(
    page_title="Quiz Rápido • Funções",
    page_icon="📐",
    layout="centered"
)

# Estilo
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.7rem;
    }
</style>
""", unsafe_allow_html=True)

# Função para gerar gráficos
def gerar_grafico(tipo, a=None, b=None):
    fig, ax = plt.subplots(figsize=(5.5, 4))
    x = np.linspace(-5, 5, 100)
    
    if tipo == "constante":
        y = np.full_like(x, b if b is not None else 2)
        cor = "#ef4444"
        titulo = f"f(x) = {b if b is not None else 2}"
    elif tipo == "linear":
        a = a if a is not None else 1.5
        y = a * x
        cor = "#3b82f6"
        titulo = f"f(x) = {a}x"
    else:
        a = a if a is not None else 1.2
        b = b if b is not None else -1
        y = a * x + b
        cor = "#8b5cf6"
        titulo = f"f(x) = {a}x + ({b})" if b < 0 else f"f(x) = {a}x + {b}"
    
    ax.plot(x, y, color=cor, linewidth=2.8)
    ax.axhline(0, color="#94a3b8", linewidth=1)
    ax.axvline(0, color="#94a3b8", linewidth=1)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-6, 6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(titulo, fontweight="bold")
    ax.plot(0, 0, "ko", markersize=5)
    fig.tight_layout()
    return fig

# Banco de perguntas
PERGUNTAS = {
    1: [
        {"tipo": "equacao", "enunciado": "Qual função está acontecendo aqui?", "conteudo": "f(x) = 7", "resposta": "constante", "explicacao": "Não depende de x. O valor é sempre 7 → Função Constante."},
        {"tipo": "equacao", "enunciado": "Qual função está acontecendo aqui?", "conteudo": "f(x) = 3x", "resposta": "linear", "explicacao": "É da forma ax (passa pela origem) → Função Linear."},
        {"tipo": "equacao", "enunciado": "Qual função está acontecendo aqui?", "conteudo": "f(x) = 2x − 5", "resposta": "afim", "explicacao": "É da forma ax + b, com a ≠ 0 e b ≠ 0 → Função Afim."},
        {"tipo": "equacao", "enunciado": "Qual função está acontecendo aqui?", "conteudo": "f(x) = −4", "resposta": "constante", "explicacao": "Valor constante → Função Constante."},
        {"tipo": "equacao", "enunciado": "Qual função está acontecendo aqui?", "conteudo": "g(x) = −1,5x", "resposta": "linear", "explicacao": "Forma ax (b = 0) → Função Linear."},
    ],
    2: [
        {"tipo": "grafico", "enunciado": "Olhe o gráfico. Qual função está acontecendo aqui?", "grafico_tipo": "constante", "params": {"b": 3}, "resposta": "constante", "explicacao": "Reta horizontal → Função Constante."},
        {"tipo": "grafico", "enunciado": "Olhe o gráfico. Qual função está acontecendo aqui?", "grafico_tipo": "linear", "params": {"a": 1.5}, "resposta": "linear", "explicacao": "Reta que passa pela origem → Função Linear."},
        {"tipo": "grafico", "enunciado": "Olhe o gráfico. Qual função está acontecendo aqui?", "grafico_tipo": "afim", "params": {"a": 1, "b": -2}, "resposta": "afim", "explicacao": "Reta inclinada que NÃO passa pela origem → Função Afim."},
        {"tipo": "grafico", "enunciado": "Olhe o gráfico. Qual função está acontecendo aqui?", "grafico_tipo": "constante", "params": {"b": -1.5}, "resposta": "constante", "explicacao": "Reta horizontal → Função Constante."},
        {"tipo": "grafico", "enunciado": "Olhe o gráfico. Qual função está acontecendo aqui?", "grafico_tipo": "linear", "params": {"a": -2}, "resposta": "linear", "explicacao": "Reta que passa pela origem → Função Linear."},
    ],
    3: [
        {"tipo": "tabela", "enunciado": "Observe a tabela. Qual função está acontecendo aqui?", "conteudo": "| x | -2 | -1 | 0 | 1 | 2 |\n| y |  5 |  5 | 5 | 5 | 5 |", "resposta": "constante", "explicacao": "O valor de y é sempre 5 → Função Constante."},
        {"tipo": "tabela", "enunciado": "Observe a tabela. Qual função está acontecendo aqui?", "conteudo": "| x | -2 | -1 | 0 | 1 | 2 |\n| y | -4 | -2 | 0 | 2 | 4 |", "resposta": "linear", "explicacao": "Passa por (0,0) e y = 2x → Função Linear."},
        {"tipo": "tabela", "enunciado": "Observe a tabela. Qual função está acontecendo aqui?", "conteudo": "| x | 0 | 1 | 2 | 3 |\n| y | 4 | 7 | 10| 13|", "resposta": "afim", "explicacao": "Aumenta de 3 em 3, mas não passa pela origem → Função Afim."},
        {"tipo": "situacao", "enunciado": "Qual função modela esta situação?", "conteudo": "Um estacionamento cobra R$ 8,00 por hora, sem taxa de entrada.", "resposta": "linear", "explicacao": "Valor = 8 × horas → Função Linear."},
        {"tipo": "situacao", "enunciado": "Qual função modela esta situação?", "conteudo": "Uma assinatura de streaming custa R$ 29,90 por mês, fixo.", "resposta": "constante", "explicacao": "Valor sempre o mesmo → Função Constante."},
        {"tipo": "situacao", "enunciado": "Qual função modela esta situação?", "conteudo": "Corrida de aplicativo: taxa fixa de R$ 5,00 + R$ 2,50 por km.", "resposta": "afim", "explicacao": "Valor = 2,5x + 5 → Função Afim."},
    ],
    4: [
        {"tipo": "equacao", "enunciado": "Desafio! Qual função é esta?", "conteudo": "f(x) = −3x + 0", "resposta": "linear", "explicacao": "−3x + 0 é o mesmo que −3x → Função Linear."},
        {"tipo": "grafico", "enunciado": "Desafio! Qual função aparece no gráfico?", "grafico_tipo": "afim", "params": {"a": 2, "b": 1}, "resposta": "afim", "explicacao": "Reta inclinada que corta o eixo y em 1 → Função Afim."},
        {"tipo": "situacao", "enunciado": "Desafio! Qual função descreve isso?", "conteudo": "A temperatura de uma sala permanece em 22 °C o tempo todo.", "resposta": "constante", "explicacao": "Temperatura fixa → Função Constante."},
        {"tipo": "tabela", "enunciado": "Desafio! Qual função gera esta tabela?", "conteudo": "| x | 1 | 2 | 3 | 4 |\n| y | 3 | 6 | 9 | 12|", "resposta": "linear", "explicacao": "y = 3x → Função Linear."},
        {"tipo": "situacao", "enunciado": "Desafio! Qual função modela?", "conteudo": "Preço = R$ 40,00 de custo fixo + R$ 12,00 por unidade.", "resposta": "afim", "explicacao": "Preço = 12x + 40 → Função Afim."},
    ]
}

# Estado da sessão
if "pontos" not in st.session_state:
    st.session_state.pontos = 0
if "fase_atual" not in st.session_state:
    st.session_state.fase_atual = None
if "indice_pergunta" not in st.session_state:
    st.session_state.indice_pergunta = 0
if "acertos_fase" not in st.session_state:
    st.session_state.acertos_fase = 0
if "respondida" not in st.session_state:
    st.session_state.respondida = False
if "ultima_resposta_correta" not in st.session_state:
    st.session_state.ultima_resposta_correta = None
if "fases_desbloqueadas" not in st.session_state:
    st.session_state.fases_desbloqueadas = {1}
if "perguntas_fase" not in st.session_state:
    st.session_state.perguntas_fase = []
if "tela" not in st.session_state:
    st.session_state.tela = "inicio"

def desbloquear_fases():
    pontos = st.session_state.pontos
    if pontos >= 15:
        st.session_state.fases_desbloqueadas.add(2)
    if pontos >= 30:
        st.session_state.fases_desbloqueadas.add(3)
    if pontos >= 50:
        st.session_state.fases_desbloqueadas.add(4)

def tela_inicio():
    st.title("📐 Quiz Rápido")
    st.subheader("Funções Constante • Linear • Afim")
    
    st.info("""
    **Como funciona?**
    - Responda: “Qual função está acontecendo aqui?”
    - Ganhe pontos a cada acerto
    - Desbloqueie novas fases
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Constante**\nf(x) = b")
    with col2:
        st.info("**Linear**\nf(x) = ax")
    with col3:
        st.warning("**Afim**\nf(x) = ax + b")
    
    st.markdown(f"### ⭐ Seus pontos: **{st.session_state.pontos}**")
    
    if st.button("🚀 Começar / Continuar", type="primary"):
        st.session_state.tela = "fases"
        st.rerun()

def tela_fases():
    st.header("Escolha a Fase")
    st.markdown(f"### ⭐ Pontos: **{st.session_state.pontos}**")
    
    desbloquear_fases()
    
    fases_info = {
        1: {"nome": "Equações", "desc": "Identifique pela lei de formação", "req": 0},
        2: {"nome": "Gráficos", "desc": "Olhe a reta e descubra", "req": 15},
        3: {"nome": "Tabelas & Situações", "desc": "Dados e contextos", "req": 30},
        4: {"nome": "Desafio Misto", "desc": "Tudo misturado", "req": 50},
    }
    
    for num, info in fases_info.items():
        desbloqueada = num in st.session_state.fases_desbloqueadas
        if desbloqueada:
            if st.button(f"**Fase {num} — {info['nome']}**\n{info['desc']}", key=f"fase_{num}"):
                st.session_state.fase_atual = num
                st.session_state.perguntas_fase = random.sample(PERGUNTAS[num], min(5, len(PERGUNTAS[num])))
                st.session_state.indice_pergunta = 0
                st.session_state.acertos_fase = 0
                st.session_state.respondida = False
                st.session_state.tela = "quiz"
                st.rerun()
        else:
            st.button(f"🔒 Fase {num} — {info['nome']} (precisa de {info['req']} pontos)", 
                      key=f"fase_{num}", disabled=True)
    
    if st.button("← Voltar ao início"):
        st.session_state.tela = "inicio"
        st.rerun()

def verificar_resposta(escolha, pergunta):
    correta = escolha == pergunta["resposta"]
    st.session_state.respondida = True
    st.session_state.ultima_resposta_correta = correta
    if correta:
        st.session_state.acertos_fase += 1
        st.session_state.pontos += 5
        desbloquear_fases()
    st.rerun()

def tela_quiz():
    fase = st.session_state.fase_atual
    perguntas = st.session_state.perguntas_fase
    idx = st.session_state.indice_pergunta
    
    if idx >= len(perguntas):
        st.session_state.tela = "resultado"
        st.rerun()
        return
    
    pergunta = perguntas[idx]
    total = len(perguntas)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Sair"):
            st.session_state.tela = "fases"
            st.rerun()
    with col2:
        st.markdown(f"**Fase {fase}** • Pergunta {idx+1}/{total}")
    with col3:
        st.markdown(f"⭐ **{st.session_state.pontos}**")
    
    st.progress(idx / total)
    st.subheader(pergunta["enunciado"])
    
    if pergunta["tipo"] == "equacao":
        st.code(pergunta["conteudo"], language=None)
    elif pergunta["tipo"] == "grafico":
        fig = gerar_grafico(pergunta["grafico_tipo"], 
                            a=pergunta["params"].get("a"), 
                            b=pergunta["params"].get("b"))
        st.pyplot(fig)
        plt.close(fig)
    elif pergunta["tipo"] == "tabela":
        st.markdown(pergunta["conteudo"])
    elif pergunta["tipo"] == "situacao":
        st.info(pergunta["conteudo"])
    
    if not st.session_state.respondida:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("Constante"):
                verificar_resposta("constante", pergunta)
        with col_b:
            if st.button("Linear"):
                verificar_resposta("linear", pergunta)
        with col_c:
            if st.button("Afim"):
                verificar_resposta("afim", pergunta)
    else:
        if st.session_state.ultima_resposta_correta:
            st.success(f"✅ Correto! {pergunta['explicacao']}")
        else:
            st.error(f"❌ Quase! A resposta certa era **{pergunta['resposta'].capitalize()}**.\n\n{pergunta['explicacao']}")
        
        if st.button("Próxima pergunta →", type="primary"):
            st.session_state.indice_pergunta += 1
            st.session_state.respondida = False
            st.rerun()

def tela_resultado():
    fase = st.session_state.fase_atual
    acertos = st.session_state.acertos_fase
    total = len(st.session_state.perguntas_fase)
    pontos_ganhos = acertos * 5
    
    if acertos == total:
        st.balloons()
        st.success("🏆 Perfeito! Você acertou todas!")
    elif acertos >= total * 0.6:
        st.success("🎉 Muito bem!")
    else:
        st.warning("💪 Continue praticando!")
    
    st.markdown(f"### Você acertou **{acertos}** de **{total}**")
    st.markdown(f"### +{pontos_ganhos} pontos | Total: **{st.session_state.pontos}** pontos")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refazer Fase"):
            st.session_state.perguntas_fase = random.sample(PERGUNTAS[fase], min(5, len(PERGUNTAS[fase])))
            st.session_state.indice_pergunta = 0
            st.session_state.acertos_fase = 0
            st.session_state.respondida = False
            st.session_state.tela = "quiz"
            st.rerun()
    with col2:
        if st.button("Continuar →", type="primary"):
            st.session_state.tela = "fases"
            st.rerun()

# Roteador
if st.session_state.tela == "inicio":
    tela_inicio()
elif st.session_state.tela == "fases":
    tela_fases()
elif st.session_state.tela == "quiz":
    tela_quiz()
elif st.session_state.tela == "resultado":
    tela_resultado()