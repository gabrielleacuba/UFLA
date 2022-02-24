import random 
# Trabalho de Algoritmo genético para encontrar o máximo da função (x*x - 3*x + 4)
# Alunos: Gabrielle Almeida Cuba && Luis Felype Fioravanti 
class Algoritmo_Genetico():

    def __init__(self, X_MIN, X_MAX, TAM_POPULACAO, TAXA_MUTACAO, TAXA_CROSSOVER, NUMERO_GERACOES):

        self.X_MIN = X_MIN
        self.X_MAX = X_MAX
        self.TAM_POPULACAO = TAM_POPULACAO
        self.TAXA_MUTACAO = TAXA_MUTACAO
        self.TAXA_CROSSOVER = TAXA_CROSSOVER
        self.NUMERO_GERACOES = NUMERO_GERACOES

        qtd_bits_x_min = len(bin(X_MIN).replace('0b', '' if X_MIN < 0 else '+'))
        qtd_bits_x_max = len(bin(X_MAX).replace('0b', '' if X_MAX < 0 else '+'))

        # o maior número de bits representa o número de bits a ser utilizado para gerar individuos

        self.num_bits = qtd_bits_x_max if qtd_bits_x_max >= qtd_bits_x_min else qtd_bits_x_min

        self.gerar_populacao()

    def gerar_populacao(self):
        #Gera uma população de um determinado tamanho com individuos que possuem um número expecífico de bits
        # inicializa uma população de "tam_população" inviduos vazios sendo ela igual a 30

        self.populacao = [[] for i in range(self.TAM_POPULACAO)]

        # preenche a população

        for individuo in self.populacao:
            # para cada individuo da população sorteia números entre "x_min" e "x_max"
            num = random.randint(self.X_MIN, self.X_MAX)
            # converte o número sorteado para formato binário com sinal
            num_bin = bin(num).replace('0b', '' if num < 0 else '+').zfill(self.num_bits)
            # transforma o número binário resultante em um vetor
            for bit in num_bin:
                individuo.append(bit)

    def converter_binario_inteiro(self, num_bin):
        num = int(''.join(num_bin), 2)
        # calcula e retorna o resultado da função objetivo
        return num**2 -3*num + 4

    def avaliarSolucoes(self):
   
        self.avaliacao = []
        for individuo in self.populacao:
            self.avaliacao.append(self.converter_binario_inteiro(individuo))

    def selecionarIndividuo(self):
        # agrupa os individuos com suas avaliações para gerar os participantes do torneio
        participantes_torneio = list(zip(self.populacao, self.avaliacao))

        individuo_1 = participantes_torneio[random.randint(0, self.TAM_POPULACAO - 1)]
        individuo_2 = participantes_torneio[random.randint(0, self.TAM_POPULACAO - 1)]

        # retorna individuo com a maior avaliação, ou seja, o vencedor do torneio
        return individuo_1[0] if individuo_1[1] >= individuo_2[1] else individuo_2[0]

    def ajustar(self, individuo):
        # Caso o individuo esteja fora dos limites de x, ele é ajustado de acordo com o limite mais próximo
        if int(''.join(individuo), 2) < self.X_MIN:
            # se o individuo é menor que o limite mínimo, ele é substituido pelo próprio limite mínimo
            ajuste = bin(self.X_MIN).replace('0b', '' if self.X_MIN < 0 else '+').zfill(self.num_bits)
            for indice, bit in enumerate(ajuste):
                individuo[indice] = bit
        elif int(''.join(individuo), 2) > self.X_MAX:
            # se o individuo é maior que o limite máximo, ele é substituido pelo próprio limite máximo
            ajuste = bin(self.X_MAX).replace('0b', '' if self.X_MAX < 0 else '+').zfill(self.num_bits)
            for indice, bit in enumerate(ajuste):
                individuo[indice] = bit

    def realizarCrossover(self, pai, mae):
        
        if random.randint(1,100) <= self.TAXA_CROSSOVER:

            # Caso o crossover seja aplicaso os pais trocam de calda e geram dois filhos
            ponto_de_corte = random.randint(1, self.num_bits - 1)
            primeiro_filho = pai[:ponto_de_corte] + mae[ponto_de_corte:]
            segundo_filho = mae[:ponto_de_corte] + pai[ponto_de_corte:]

            self.ajustar(primeiro_filho)
            self.ajustar(segundo_filho)    
        else:
            # caso contrário os filhos são cópias exatas dos pais
            primeiro_filho = pai[:]
            segundo_filho = mae[:]

        return (primeiro_filho, segundo_filho)

    def realizarMutacao(self, individuo):

        tabela_mutacao = str.maketrans('+-01', '-+10')

        # caso a taxa de mutação seja atingida, ela é realizada em um bit aleatório
        if random.randint(1,100) <= self.TAXA_MUTACAO:
            bit = random.randint(0, self.num_bits - 1)
            individuo[bit] = individuo[bit].translate(tabela_mutacao)

        # se o individuo estiver fora dos limites de x, ele é ajustado de acordo com o
        # limite mais próximo
        self.ajustar(individuo)

    def encontrar_mais_apto(self):
        #Busca o individuo com a melhor avaliação dentro da população
    
        # agrupa os individuos com suas avaliações para gerar os candidatos
        candidatos = list(zip(self.populacao, self.avaliacao))
        # retorna o candidato com a melhor avaliação, ou seja, o mais apto da população
        return max(candidatos, key=lambda elemento: elemento[1])


def main():
    algoritmoGenetico = Algoritmo_Genetico(-10, 10, 4, 1, 70, 5)
    algoritmoGenetico.avaliarSolucoes()
    for i in range(algoritmoGenetico.NUMERO_GERACOES):

        print( 'Resultado {}: {}'.format(i, algoritmoGenetico.encontrar_mais_apto()) )

        nova_populacao = []
        while len(nova_populacao) < algoritmoGenetico.TAM_POPULACAO:

            pai = algoritmoGenetico.selecionarIndividuo()
            mae = algoritmoGenetico.selecionarIndividuo()

            primeiro_filho, segundo_filho = algoritmoGenetico.realizarCrossover(pai, mae)

            algoritmoGenetico.realizarMutacao(primeiro_filho)
            algoritmoGenetico.realizarMutacao(segundo_filho)

            nova_populacao.append(primeiro_filho)
            nova_populacao.append(segundo_filho)

        # substitui a população antiga pela nova e realiza sua avaliação
        algoritmoGenetico.populacao = nova_populacao
        algoritmoGenetico.avaliarSolucoes()

    print( 'Resultado {}: {}'.format(i+1, algoritmoGenetico.encontrar_mais_apto()) )

    return 0

if __name__ == '__main__':
    main()

