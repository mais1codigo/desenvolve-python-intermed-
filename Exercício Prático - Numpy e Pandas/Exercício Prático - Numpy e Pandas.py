######Conversões de tipo e salvamento do DataFrame

df['data'] = pd.to_datetime(df['data'])
df[['gols_1', 'gols_2', 'comparecimento', 'ano']] = df[['gols_1', 'gols_2', 'comparecimento', 'ano']].astype(int)
df['rodada'] = df['rodada'].astype('category')

df.to_csv('wc_formatado.csv', index=False)
df.info()


######ogo com maior audiência 
maior_audiencia = df.loc[df['comparecimento'].idxmax()]
print(maior_audiencia)


######Contagem de Copas Masculinas e Femininas 
copas = df.groupby('copa')['ano'].nunique()
print(f"Masculina: {copas.get('Masculina', 0)}")
print(f"Feminina: {copas.get('Feminina', 0)}")


######Top 5 países por participação
participacao = df.groupby(['time_1', 'copa']).size().reset_index(name='num_copas')
top5 = participacao.sort_values(by='num_copas', ascending=False).groupby('copa').head(5)
print(top5)


######Total de gols por país
gols = df.groupby('time_1')['gols_1'].sum() + df.groupby('time_2')['gols_2'].sum()
gols = gols.reset_index(name='total_gols').sort_values(by='total_gols', ascending=False)
print(gols)




########País com mais cartões amarelos 
def contar_cartoes(cartoes):
    if pd.isna(cartoes):
        return 0
    return len(cartoes.split('|'))

df['num_cartoes_1'] = df['cartao_amarelo_1'].apply(contar_cartoes)
df['num_cartoes_2'] = df['cartao_amarelo_2'].apply(contar_cartoes)

cartoes = df.groupby('time_1')['num_cartoes_1'].sum() + df.groupby('time_2')['num_cartoes_2'].sum()
cartoes = cartoes.reset_index(name='cartoes_amarelos').sort_values(by='cartoes_amarelos', ascending=False)
print(cartoes.head(10))




#########Top 10 jogadores com mais gols
from collections import defaultdict

def extrair_jogadores(gols):
    if pd.isna(gols):
        return []
    return [gol.split(' · ')[0] for gol in gols.split('|')]

gols_dict = defaultdict(int)

for col in ['gols_1_detalhes', 'gols_2_detalhes', 'gols_1_penalti', 'gols_2_penalti']:
    df[col].apply(lambda x: [gols_dict[jogador] += 1 for jogador in extrair_jogadores(x)])

top10_jogadores = pd.DataFrame(gols_dict.items(), columns=['jogador(a)', 'num_gols']).sort_values(by='num_gols', ascending=False).head(10)
print(top10_jogadores)