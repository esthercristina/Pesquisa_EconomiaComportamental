#Bibliotecas
from scipy.stats import chi2_contingency
from scipy.stats import spearmanr
from matplotlib.gridspec import GridSpec

import matplotlib.pyplot as  plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec




# Carregamento da planilha
arquivo = "Pesquisa.xlsx"
df = pd.read_excel(arquivo)
df.columns = df.columns.str.strip()  # <- remove espaços extras nos nomes das colunas

#Para testar se está puxando a base corretamente
print ("Dimensões da base:",df.shape)
print ("\nColunas:")
print (df.columns.tolist())

print ("\nAmostra dos dados:")
print (df.head())

#--------------------1. VIÉS DE ANCORAGEM ----------------------------------
     
    #Comparar percepção x comportamento 
    #Teste Qui-quadrado (p < 0.05) Há diferença significativa entre percepção x comportamento?
    #Gráfico

print('\n'+'='*50)
print('Viés: Ancoragem')

# Selecinando as colunas binárias de ancoragem
Colunas_ancoragem = ['R_enviesada_ancoragem1','R_enviesada_ancoragem2']
#Soma de respostas enviesadas ou não (por linha)
df['Total_ancoragem'] = df[Colunas_ancoragem].sum(axis=1)
#Define como "enviesado" quem teve pelo menos 1 resposta enviesada
df['Grupo_ancoragem_calculado'] = df['Total_ancoragem'].apply(lambda x: 1 if x >= 1 else 0)
#Contagem Geral
contagem = df['Grupo_ancoragem_calculado'].value_counts().sort_index()
print('\nDistribuição de enviesamento por ancoragem:')
print(f'Não enviesados (0): {contagem[0]}')
print(f'Enviesados (1): {contagem[1]}')

#PORCENTAGEM
porcentagem = df['Grupo_ancoragem_calculado'].value_counts(normalize=True).sort_index()*100
print('\nPorcentagem de Respostas:')
print(f'Não enviesados (0): {porcentagem[0]:.2f}%')
print(f'Enviesados (1): {porcentagem[1]:.2f}%')

#VALIDAÇÃO
#1---Comparação com a planilha (percepção e comportamento)
comparacao = pd.crosstab(df['Grupo_ancoragem'],df['Grupo_ancoragem_calculado'])
print('\nMatriz de Confusão (Percepção vs Comportamento):')
print(comparacao)
#2---Teste Qui-quadrado (x2 - identificador de diferença significativa no que foi observado em uma amostra e o que seria esperado)
chi2, p, dof, expected = chi2_contingency(comparacao)
print('\nResultado do teste Qui-Quadrado:')
print(f'Estatística Qui²: {chi2:.4f}')
if p < 0.05:
    print('>> Há diferença significativa entre percepção e comportamento (p < 0.05)')
else: 
    print('>> Não há diferença estatística significativa (p >= 0.05)')

#3---Gráfico comparativo (barra)
ax = comparacao.plot(kind='bar', stacked=True, colormap='Set2', figsize=(6,5))
total1 = len(df) #contagem de linhas
# Adiciona os rótulos de quantidade em cada barra (%)
for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        percentual = 100 * altura/total1
        ax.text(p.get_x() + p.get_width() / 2, 
            altura + 0.4, 
            f'{percentual:.2f}%', 
            ha= 'center', fontsize = 8)

# Ajustes visuais            
plt.title("Percepção vs Comportamento - Viés de Ancoragem")
plt.xlabel("Percepção")
plt.ylabel("Número de pessoas")
plt.legend(title="Comportamento ", labels=["Não enviesado", "Enviesado"])
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

#-------------------2. VIÉS DE AVERSÃO A PERDA --------------------------------------
     
    #Comparar percepção x comportamento 
    #Teste Qui-quadrado
    #Gráfico


print('\n' + '='*50)
print("Viés: Aversão à Perda")

#Soma dos comportamentos enviesados
colunas_aversao = ['R_enviesada_aversaoperda1','R_enviesada_aversaoperda2']
df['Total_aversaoperda'] = df[colunas_aversao].sum(axis=1)
df['Grupo_aversaoperda_calculado'] = df['Total_aversaoperda'].apply(lambda x:1 if x>=1 else 0)
#Comparar com a percepção
comparacao_aversao = pd.crosstab(df['Grupo_aversaoperda'],df['Grupo_aversaoperda_calculado'])
print('\nMatriz de Confusão (Percepção vs Comportamento):')
print(comparacao_aversao)
#Teste qui-quadrado
chi2,p,dof,expected = chi2_contingency(comparacao_aversao)
print('\nResultado do teste Qui-quadrado:')
print(f'Estatística Qui²: {chi2:.4f}')
print(f'p-valor: {p:.4f}')
if p < 0.05:
    print('>> Há diferença significativa entre percepção e comportamento (p < 0.05)')
else:
    print('>> Não há diferença estatística significativa (p >=0.05)')
#Gráfico
ax = comparacao_aversao.plot(kind='bar',stacked=True,colormap='Set2',figsize=(6,5))
total2 = len(df)
#rótulo
for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        percentual = 100 * altura / total2
        ax.text(p.get_x() + p.get_width() / 2,
                altura + 0.4,
                f'{percentual:.2f}%',
                ha='center', fontsize = 8)

plt.title("Percepção vs Comportamento - Viés de Aversão à Perda")
plt.xlabel("Percepção ")
plt.ylabel("Número de pessoas")
plt.legend(title="Comportamento", labels=['Não enviesado', 'Enviesado'])
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

#-------------------3. VIÉS DE ENQUADRAMENTO --------------------------------------
     
    #Comparar percepção x comportamento 
    #Teste Qui-quadrado
    #Gráfico

print('\n'+'='*50)
print("Viés: Enquadramento")

#Soma dos comportamentos enviesados
colunas_enquadramento = ['R_enviesada_enquadramento1','R_enviesada_enquadramento2'] #para chamar as colunas
df['Total_enquadramento'] = df[colunas_enquadramento].sum(axis=1)
df['Grupo_enquadramento_calculado'] = df['Total_enquadramento'].apply(lambda x:1 if x >=1 else 0)
#Comparar percepção
comparacao_enquadramento = pd.crosstab(df['Grupo_enquadramento'],df['Grupo_enquadramento_calculado'])
print('\nMatriz de Coonfusão (Percepção vs Comportamento):')
print(comparacao_enquadramento)
#Teste qui-quadrado
chi2,p,dof,expected = chi2_contingency(comparacao_enquadramento)
print('\nResultado do teste Qui-quadrado:')
print(f'Estatística Qui²: {chi2:.4f}')
print(f'p-valor: {p:.4f}')
if p < 0.05:
    print('>> Há diferença significativa entre percepção e comportamento (p < 0.05)')
else:
    print('>> Não há diferença estatística significativa (p >= 0.05)')
#Gráfico
ax = comparacao_enquadramento.plot(kind='bar',stacked=True,colormap='Set2',figsize=(6,5))
total3 = len(df)
#rótulo
for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        percentual = 100 * altura / total3
        ax.text(p.get_x() + p.get_width() / 2,
                altura + 0.4,
                f'{percentual:.2f}%',
                ha='center', fontsize = 8)
#ajustes visuais
plt.title("Percepção vs Comportamento - Viés de Enquadramento")
plt.xlabel("Percepção ")
plt.ylabel("Número de pessoas")
plt.legend(['Não enviesado', 'Enviesado'], title="Comportamento ")
plt.xticks(rotation=15)



plt.tight_layout()
plt.show()

#-------------------4. VIÉS DE CONTABILIDADE MENTAL --------------------------------------
     
    #Entender os padrões das respostas abertas 
    #Classificação manual
    #Criação do grupo identificando as respostas emocionais
    #Comparar percepção vs comportamento
    #Gráfico
#PARTE 1
#classificação - contmental2 - criação de coluna
print('\n'+'='*50)
print('Classificação Contabilidade Mental2')
#Palavras-chave que indicam EMOÇÃO
padroes_emocionais = [
    'medo','consumista','angustiad','triste','tranquil','nervos','ansios','não posso dever',
    'preocup','melhor','aliviad','sofro','culpa','pressão','compraria','recompensa','lazer',
    'merecimento','espairecer','hoje','única','comprar','esperar'
]
#função de classificação
def classificar_emocional(texto):
    if pd.isnull(texto):
        return 0 
    texto = texto.lower()
    for palavra in padroes_emocionais:
        if palavra in texto:
            return 1
    return 0
#rodar a função
df['R_enviesado_ContMental2'] = df['ContMental_2'].apply(classificar_emocional)


#calcular o total enviesado de contabilidade mental
#calcula o grupo total baseado nas 2 respostas
df['Total_contmental'] = df[['R_enviesado_ContMental1','R_enviesado_ContMental2']].sum(axis=1)
df['Grupo_contmental_calculado'] = df['Total_contmental'].apply(lambda x:1 if x >= 1 else 0)

#PARTE 2-FINAL
print('\n' + '='*50)
print("Viés: Contabilidade Mensal (Consolidado)")

#Calculo total
df['Total_contmental'] = df[['R_enviesado_ContMental1','R_enviesado_ContMental2']].sum(axis=1)
df['Grupo_contmental_calculado'] = df['Total_contmental'].apply(lambda x:1 if x >= 1 else 0)
#Contagem absoluta
contagem_contmental = df['Grupo_contmental_calculado'].value_counts().sort_index()
print('\nDistribuição de enviesamento (comportamento):')
print(f'Não enviesados (0): {contagem_contmental[0]}')
print(f'Enviesados (1): {contagem_contmental[1]}')
#Porcentagem
porcentagem_contmental = df['Grupo_contmental_calculado'].value_counts(normalize=True).sort_index()*100
print('\nPorcentagens:')
print(f'Não enviesados (0): {porcentagem_contmental[0]:.2f}%')
print(f'Enviesados (1): {porcentagem_contmental[1]:.2f}%')
#Gráfico com percentual na barra
plt.figure(figsize=(5,4))
sns.countplot(x='Grupo_contmental_calculado', data=df, palette='Set2')
plt.title('Comportamento - Viés de Contabilidade Mental')
plt.xlabel('Percepção')
plt.ylabel('Número de pessoas')
plt.xticks([0,1],['Racional','Emocional'])
total = len(df)
ax = sns.countplot(x = 'Grupo_contmental_calculado', data=df, palette='Set2')

for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        percentual = 100 * altura/total
        ax.text(p.get_x() + p.get_width() / 2, 
            altura + 0.5, 
            f'{percentual:.2f}%', 
            ha= 'center', fontsize = 8)
plt.tight_layout()
plt.show()

#---------------------------------------------------------------------------------------------
#--------------------------------IDADE X GENÊRO-------------------------------------------------

print('\n' + '='*50)
print('Faixa Etária X Gênero')

# Criar tabela de frequência
tabela = pd.crosstab(df['Faixa_Etária'], df['Gênero'])

# Criar figura com 2 colunas (gráfico e tabela)
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

# GRÁFICO DE BARRAS EMPILHADAS COM PORCENTAGEM
ax0 = plt.subplot(gs[0])
bottom_values = [0] * len(tabela)  # posição da base para cada faixa etária
colors = sns.color_palette("Set2", n_colors=len(tabela.columns))

for i, genero in enumerate(tabela.columns):
    valores = tabela[genero].values
    barras = ax0.bar(tabela.index, valores, bottom=bottom_values, label=genero, color=colors[i])
    
    # Inserindo percentual em cada segmento
    for j, (b, val) in enumerate(zip(bottom_values, valores)):
        total = tabela.iloc[j].sum()
        if val > 0:
            percentual = (val / total) * 100
            ax0.text(j, b + val / 2, f'{percentual:.1f}%', ha='center', va='center', fontsize=9, color='black')
    
    bottom_values = [b + v for b, v in zip(bottom_values, valores)]

ax0.set_title('Distribuição de Gênero por Faixa Etária (%)')
ax0.set_xlabel('Faixa Etária')
ax0.set_ylabel('Número de Pessoas')
ax0.legend(title='Gênero')
ax0.tick_params(axis='x', rotation=45)

# TABELA DE FREQUÊNCIA
tabela_com_total = tabela.copy()
tabela_com_total['Total'] = tabela.sum(axis=1)
tabela_com_total = tabela_com_total.reset_index()

ax1 = plt.subplot(gs[1])
ax1.axis('off')
tabela_plot = ax1.table(cellText=tabela_com_total.values,
                        colLabels=tabela_com_total.columns,
                        cellLoc='center',
                        loc='center')
tabela_plot.auto_set_font_size(False)
tabela_plot.set_fontsize(9)
tabela_plot.scale(1.2, 1.5)

plt.tight_layout()
plt.show()

#---------------------------------------------------------------------------------------------
#--------------------------------ESCOLARIDADE X RENDA-------------------------------------------------

print('\n' + '='*50)
print('Renda X Escolaridade')

# Dicionário para renomear os níveis da Renda Ordinal
renda_labels = {
    0: 'Prefiro não dizer',
    1: 'Baixa',
    2: 'Média',
    3: 'Alta'
}
df['Renda_Ordinal_Label'] = df['Renda_Ordinal'].map(renda_labels)

# Tabela de frequência absoluta e percentual
frequencia = df['Renda_Ordinal_Label'].value_counts().rename_axis('Renda').reset_index(name='Frequência')
frequencia['%'] = round(frequencia['Frequência'] / frequencia['Frequência'].sum() * 100, 1).astype(str) + '%'

# layout com 2 colunas gráfico e tabela
fig = plt.figure(figsize=(10, 5))
gs = GridSpec(1, 2, width_ratios=[2, 1])

# GRÁFICO DE BARRAS
ax0 = fig.add_subplot(gs[0])
ax = sns.countplot(x='Renda_Ordinal_Label', data=df, palette='Set2', order=renda_labels.values(), ax=ax0)

# Rótulo de percentual nas barras
total = len(df)
for p in ax.patches:
    altura = p.get_height()
    percentual = 100 * altura / total
    ax.annotate(f'{percentual:.1f}%', 
                (p.get_x() + p.get_width() / 2, altura),
                ha='center', va='bottom', fontsize=10)

ax.set_title('Distribuição da Renda Ordinal')
ax.set_ylabel('Frequência')
ax.set_xlabel('Renda')
ax.tick_params(axis='x', rotation=15)

# TABELA DE FREQUÊNCIAS
ax1 = fig.add_subplot(gs[1])
ax1.axis('off')
tabela = ax1.table(cellText=frequencia.values,
                   colLabels=frequencia.columns,
                   cellLoc='center',
                   loc='center')
tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1.2, 1.5)  # Ajuste do tamanho da tabela

plt.tight_layout()
plt.show()


#---------------------------------------------------------------------------------------------
#--------------------------------RENDA X IDADE-------------------------------------------------

print('\n' + '='*50)
print('Faixa Etária x Renda')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.gridspec import GridSpec

# Planilha -carregamento
df = pd.read_excel("Pesquisa.xlsx")

# filtro de colunas
df = df[['Faixa_Etária', 'Renda_Ordinal']].dropna()

# Níveis da Renda para legenda
renda_labels = {
    0: 'Prefiro não dizer',
    1: 'Baixa',
    2: 'Média',
    3: 'Alta'
}
df['Renda_Label'] = df['Renda_Ordinal'].map(renda_labels)

# tabela contagem absoluta
contagem = pd.crosstab(df['Faixa_Etária'], df['Renda_Label'])

#tabela percentuais
percentual = contagem.div(contagem.sum(axis=1), axis=0) * 100
percentual = percentual.round(1).astype(str) + '%'

# layout, gráfico e tabelas
fig = plt.figure(figsize=(12, 5))
gs = GridSpec(1, 2, width_ratios=[2, 1])

# GRÁFICO DE BARRAS 
ax0 = fig.add_subplot(gs[0])
cores = plt.get_cmap('Set2').colors
contagem.plot(kind='bar', stacked=True, ax=ax0, color=cores)

ax0.set_title('Distribuição da Renda por Faixa Etária', fontsize=13)
ax0.set_xlabel('Faixa Etária')
ax0.set_ylabel('Número de Pessoas')
ax0.legend(title='Renda')
ax0.tick_params(axis = 'x', rotation=15)

# rótulo nas barras (%)
totais = contagem.sum(axis=1)
for i, faixa in enumerate(contagem.index):
    y_base = 0
    for j, renda in enumerate(contagem.columns):
        valor = contagem.loc[faixa, renda]
        if valor > 0:
            perc = valor / totais[faixa] * 100
            ax0.text(i, y_base + valor / 2, f'{perc:.1f}%', 
                     ha='center', va='center', fontsize=9)
            y_base += valor

# tabela
ax1 = fig.add_subplot(gs[1])
ax1.axis('off')
tabela_exibicao = contagem.astype(str) + ' (' + percentual + ')'
tabela_formatada = ax1.table(cellText=tabela_exibicao.values,
                              rowLabels=tabela_exibicao.index,
                              colLabels=tabela_exibicao.columns,
                              loc='center')
tabela_formatada.auto_set_font_size(False)
tabela_formatada.set_fontsize(10)
tabela_formatada.scale(1.2, 1.3)

plt.tight_layout()
plt.show()

#---------------------------------------------------------------------------------------------
#--------------------------------RENDA X contmental-------------------------------------------------
print('\n' + '='*50)
print('Renda x Contabilide Mental')

# Carregamento da planilha
df = pd.read_excel("Pesquisa.xlsx")
df.columns = df.columns.str.strip()  # Remove espaços extras

# variáveis com base nas palavras emocionais
padroes_emocionais = [
    'medo','consumista','angustiad','triste','tranquil','nervos','ansios','não posso dever',
    'preocup','melhor','aliviad','sofro','culpa','pressão','compraria','recompensa','lazer',
    'merecimento','espairecer','hoje','única','comprar','esperar'
]

def classificar_emocional(texto):
    if pd.isnull(texto):
        return 0 
    texto = texto.lower()
    for palavra in padroes_emocionais:
        if palavra in texto:
            return 1
    return 0

# Criação da coluna
if 'R_enviesado_ContMental2' not in df.columns:
    df['R_enviesado_ContMental2'] = df['ContMental_2'].apply(classificar_emocional)

# Agrupamento
df['Total_contmental'] = df[['R_enviesado_ContMental1', 'R_enviesado_ContMental2']].sum(axis=1)
df['Grupo_contmental_calculado'] = df['Total_contmental'].apply(lambda x: 1 if x >= 1 else 0)

# Dicionário de rótulos de renda
renda_labels = {
    0: 'Prefiro não dizer',
    1: 'Baixa',
    2: 'Média',
    3: 'Alta'
}

# Tabela cruzada
tabela = pd.crosstab(df['Renda_Ordinal'], df['Grupo_contmental_calculado'])
tabela.rename(index=renda_labels, columns={0: 'Racional', 1: 'Enviesado'}, inplace=True)

# Gráfico de barras com percentuais
fig, ax = plt.subplots(figsize=(8, 5))
tabela.plot(kind='bar', stacked=True, colormap='Set2', ax=ax)

ax.set_title("Contabilidade Mental por Renda")
ax.set_xlabel("Renda")
ax.set_ylabel("Número de Pessoas")
ax.legend(title="Comportamento")
ax.tick_params(axis='x', rotation=15)  # Rotação dos rótulos no eixo X

# Rótulos percentuais nas barras
totais = tabela.sum(axis=1)
for i, (idx, row) in enumerate(tabela.iterrows()):
    acumulado = 0
    total = totais[idx]
    for valor in row:
        if valor > 0:
            percent = valor / total * 100
            ax.text(i, acumulado + valor / 2, f'{percent:.1f}%', ha='center', va='center', fontsize=9)
            acumulado += valor

plt.tight_layout()
plt.show()



# Criação da tabela 
contingencia = pd.crosstab(df['Renda_Ordinal'], df['Grupo_contmental_calculado'])

# Exibição da tabela 
print("Tabela de Contingência:")
print(contingencia)

# Aplicação do teste
chi2, p, dof, expected = chi2_contingency(contingencia)

# Exibição dos resultados
print("\nResultado do Teste Qui-Quadrado:")
print(f"Chi²: {chi2:.4f}")
print(f"p-valor: {p:.4f}")
print(f"Graus de Liberdade: {dof}")
print("Frequências Esperadas:")
print(expected)

if p < 0.05:
    print("\n>> Há associação estatística significativa entre renda e comportamento (p < 0.05).")
else:
    print("\n>> Não há associação estatística significativa entre renda e comportamento (p >= 0.05).")


#---------------------------------------------------------------------------------------------
#--------------------------------DEMOGRAFIA-------------------------------------------------
print('\n' + '='*50)
print('Demografia')

# Contagem e percentual por faixa etária
faixa_etaria = df['Faixa_Etária'].value_counts().sort_index()
faixa_etaria_percentual = (faixa_etaria / len(df)) * 100
print("Distribuição por faixa etária:")
for faixa, count in faixa_etaria.items():
    print(f"- {faixa}: {count} participantes ({faixa_etaria_percentual[faixa]:.1f}%)")

# Contagem e percentual por gênero
genero = df['Gênero'].value_counts()
genero_percentual = (genero / len(df)) * 100
print("\nDistribuição por gênero:")
for g, count in genero.items():
    print(f"- {g}: {count} participantes ({genero_percentual[g]:.1f}%)")

# Contagem e percentual por escolaridade
escolaridade = df['Escolaridade'].value_counts()
escolaridade_percentual = (escolaridade / len(df)) * 100
print("\nDistribuição por escolaridade:")
for esc, count in escolaridade.items():
    print(f"- {esc}: {count} participantes ({escolaridade_percentual[esc]:.1f}%)")

# Contagem e percentual por faixa de renda (coluna 'Renda_Ordinal')
renda = df['Renda_Ordinal'].value_counts().sort_index()
renda_labels = {
    0: 'Prefiro não dizer',
    1: 'Baixa',
    2: 'Média',
    3: 'Alta'
}
renda_percentual = (renda / len(df)) * 100
print("\nDistribuição por faixa de renda:")
for cod, count in renda.items():
    label = renda_labels.get(cod, f"Categoria {cod}")
    print(f"- {label}: {count} participantes ({renda_percentual[cod]:.1f}%)")


#---------------------------------------------------------------------------------------------
#--------------------------------aversão a perda x renda-------------------------------------------------
print('\n' + '='*50)
print('Aversão a perda x renda')




# Supondo que:
# - 'aversao_perda' é uma coluna categórica com valores como 'completamente enviesado', 'impulso sem percepção', etc.
# - 'renda' é uma coluna categórica com faixas de renda

# Tabela cruzada
tabela = pd.crosstab(df['Renda_Categórica'], df['Grupo_aversaoperda'], normalize='index') * 100
tabela = tabela[['Completamente enviesado', 'Impulso sem percepção', 'Racional', 'Resistência racional']]  # Ordenar se necessário
tabela.index = tabela.index.str.replace('NS', 'Não informado')

# Cores 
colors = ['#3b0a45', '#356c94', '#55aa7f', '#f7dc52']

#  gráfico de barras agrupadas
fig, ax = plt.subplots(figsize = (10,6))

bottom = [0] * len(tabela)
for i, col in enumerate(tabela.columns):
    ax.bar(tabela.index, tabela[col], bottom=bottom, label=col, color=colors[i])
    for j, val in enumerate(tabela[col]):
        if val > 5:  # só mostra se for maior que 5% para não poluir 
            ax.text(j, bottom[j] + val / 2, f'{val:.2f}%', ha='center', va='center', fontsize=9, color='white')
    bottom = [bottom[j] + tabela[col].iloc[j] for j in range(len(tabela))]

ax.set_title('Distribuição do Viés de Aversão à Perda por Faixa de Renda')
ax.set_ylabel('% dos Respondentes')
ax.set_xlabel('Faixa de Renda')
ax.legend(
    title='Classificação Comportamental',
    bbox_to_anchor=(1.02, 0.5),
    loc='center left',
    borderaxespad=0
)
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#---------------------------------------------------------------------------------------------
#--------------------------------escolaridade x enquadramento-------------------------------------------------

print('\n' + '='*50)
print('Enquadramento x Escolaridade')

# DataFrame de exemplo
data = {
    'Escolaridade': ['Médio', 'Superior', 'Pós', 'Médio', 'Superior', 'Pós', 'Médio', 'Superior', 'Pós'] * 5,
    'Grupo_enquadramento': ['Completamente enviesado', 'Racional', 'Completamente enviesado',
                            'Racional', 'Resistência racional', 'Impulso sem percepção',
                            'Completamente enviesado', 'Racional', 'Resistência racional'] * 5
}
df = pd.DataFrame(data)

# Contagem por grupo
grouped = df.groupby(['Escolaridade', 'Grupo_enquadramento']).size().unstack(fill_value=0)

#percentual
percentual = grouped.div(grouped.sum(axis=1), axis=0) * 100

# Plot
ax = percentual.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20c')

# Rótulos em cada barra
for i, row in enumerate(percentual.values):
    bottom = 0
    for j, val in enumerate(row):
        if val > 0:
            ax.text(i, bottom + val / 2, f'{val:.1f}%', ha='center', va='center', fontsize=8)
            bottom += val

# Ajustes finais
plt.title('Distribuição do Viés de Enquadramento por Escolaridade')
plt.ylabel('% dos Respondentes')
plt.xlabel('Escolaridade')
plt.legend(title='Classificação Comportamental', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()
