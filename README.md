# a-star-searching
- Instalar o Python
- Rodar usando "python main.py"

## TODO
- Gerar jogo aleatóriamente
    - 2/3 guardas
    - 4/7 bloqueios
    - 1 saída
    - Não gerar componentes sobre componentes já gerados
    - Não bloquear totalmente a saída
- Solicitar entrada do programa (estadoInicial) a cada rodada
    - Não permitir entrada sobre componentes já gerados
- Definir as heurísticas
    - admissível
    - não admissível
- Lógica de fim de jogo (3 tentativas)
    - chegar na saída -> vitória na rodada
    - andar sobre um guarda -> derrota na rodada
    - primeira vitória -> vencedor geral
    - nenhuma vitória -> perdedor geral
- Saída do programa
    - Lista Aberta
    - Lista Fechada
    - Árvore