#Projeto Wumpus
Este projeto foi desenvolvido como parte das aulas de Algoritmos em Python, com o objetivo de estudar, testar e comparar diferentes estratégias de navegação em uma matriz 8x8 simulando o famoso jogo do Wumpus, onde nos criamos também o jogo e todos os elementos dele: monstros, pedras, baús(Três baús: Vazio, Armadilha onde ele morre e por fim o verdadeiro que vence o jogo), e mapa do tesouro (Chave onde tem a localização do baú certo).

Objetivo
O jogador (algoritmo) precisa encontrar uma chave e levá-la até um baú, evitando ao máximo cair em armadilhas como o monstro Wumpus. O projeto consistiu na implementação de quatro algoritmos diferentes para resolver este problema, cada um com uma abordagem única.

Algoritmos Implementados
## 1. Algoritmo Aleatório
Descrição: O agente se move escolhendo direções aleatórias (cima, baixo, esquerda, direita).

Vantagens: Simples de implementar.

Desvantagens: Altamente ineficiente, tende a se perder ou cair em armadilhas com frequência.

## 2. Algoritmo "Monstro"
Descrição: Tenta evitar ao máximo passar próximo ao Wumpus.

Estratégia: Baseia-se na percepção de perigo ao redor e prioriza caminhos mais seguros, mesmo que mais longos.

Vantagens: Menos mortes comparado ao aleatório.

Desvantagens: Pode ignorar o caminho mais curto ou eficiente.

## 3. Algoritmo de Menor Distância
Descrição: Procura sempre a menor distância até a chave, e depois até o baú.

Estratégia: Utiliza heurísticas simples (como distância Manhattan ou BFS).

Vantagens: Mais eficiente em termos de tempo e movimentos.

Desvantagens: Pode não considerar armadilhas ou perigos ao redor.

## 4. Algoritmo com Árvore de Decisão (Melhor Algoritmo)
Descrição: Este foi o algoritmo mais completo e eficaz desenvolvido no projeto.

Estratégia:

Analisa toda a matriz 8x8 como um grafo.

Mapeia completamente o ambiente e calcula o caminho ideal considerando todos os fatores (chave, baú, monstros).

Garante quase 100% de sucesso nas execuções.

Vantagens: Extremamente eficiente e preciso.

Desvantagens: Mais complexo de implementar.

Conclusão
O projeto serviu como uma excelente oportunidade para aplicar conceitos de algoritmos de busca, árvores, grafos e lógica de decisão. Entre os quatro, o algoritmo com árvore de decisão se destacou como o mais robusto, conseguindo traçar o caminho ideal com altíssima taxa de sucesso.

Tecnologias
Python
