import datetime #Biblioteca para acessar as horas
import json #Biblioteca para formatar os blocos
import hashlib #Biblioteca para criptografar os blocos

class Blockchain:
    def __init__(self, dificuldade): #Inicializa os atributos e os métodos da classe
        self.chain = [] #Lista com todos os blocos
        self.dificuldade = dificuldade #Nível de criptográfia do Hash
        self.create_blockchain(proof=1, previous_hash='0',dados='Bloco Genesis') #Cria o bloco genesis

    def create_blockchain(self, proof, previous_hash, dados): #Função que cria o bloco
        block = { #A estrutura de dados do bloco
            'index': len(self.chain) + 1, #Posição do bloco na Blockchain
            'timestamp': str(datetime.datetime.now()), #A hora que o bloco foi criado
            'proof': proof, #A prova de trabalho
            'previous_hash': previous_hash, #O hash do bloco anterior
            'dados': dados
        }
        self.chain.append(block) #Adiciona na lista de blocos
        return block #Retorna o bloco individualmente

    def get_previous_block(self): #Função que busca o blco anterior anterior
        last_block = self.chain[-1] #Acessa o último bloco da lista...
        return last_block #E o retorna

    def proof_of_work(self, previous_proof): #Função para minerar um bloco
        new_proof = 1 #Armazena a prova enviada pelos trabalhadores
        check_proof = False #Status da prova de trabalho
        while check_proof is False: #Verifica o status
            #Gera um algoritmo usando o hash anterior para os mineradores
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == self.dificuldade: #Verifica se o problema foi resolvido
                check_proof = True
            else: #Caso não...
                new_proof += 1 #Dá outra chance para os mineradores
        return new_proof 

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode() #Formata o bloco...
        return hashlib.sha256(encoded_block).hexdigest() #E o criptografa, retornando o hash

    def is_chain_valid(self): #Verifica se a blockchain é valida
        previous_block = self.chain[0] #Começa com o hash do bloco genesis
        block_index = 1 #Váriavel para percorrer a blockchain
        while block_index < len(self.chain):
            block = self.chain[block_index] #Pega o bloco atual
            if block["previous_hash"] != self.hash(previous_block): #Confere se o bloco tem o mesmo hash do anterior
                return False #Caso sim, ele invalida a blockchain
            previous_proof = previous_block['proof'] #Pega a prova de trabalho do bloco anterior
            current_proof = block['proof'] #Pega a prova de trabalho do bloco atual
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != self.dificuldade: #Confere se a operação hasf foi inválida
                return False #Caso sim, ele invalida a blockchain
            previous_block = block #Passa o bloco atual como anterior...
            block_index += 1 #E passa para o próximo
        return True

if __name__ == '__main__':
    dificuldade = str(input("Insira como você deseja iniciar o hash (dificuldade): ")) #Requista a dificuldade da criptográfia para o úsuario...   
    blockchain = Blockchain(dificuldade) #E envia ao instânciar um objeto da classe Blockchain
    
    check = 'S' #Cria uma váriavel de vericação
    while check == 'S': #Mantêm o úsuario em um loop para criar mais de um bloco
       #Prova de Trabalho 
        previous_block = blockchain.get_previous_block() #Resgata o último bloco...
        previous_proof = previous_block['proof'] #E sua prova de trabalho
        proof = blockchain.proof_of_work(previous_proof) #Realiza uma nova prova usando a anterior
        
        previous_hash = blockchain.hash(previous_block) #Resgata o hash anterior
        dados = str(input("Digite os dados do bloco: "))  #Requisita o dado a ser armazenado ao usuário
        block = blockchain.create_blockchain(proof, previous_hash, dados) #Cria o bloco com as informações reunidas e adiciona na blockchain
        
        response = { #Estrutura os dados da mineração...
                'aviso': 'Bloco Minerado!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
        for key, data in response.items(): #E apresenta na tela
            print(key + ':', data )

        check = str(input("\nDeseja continuar adicionando novos blocos? (S/N): ")) #Confere se quer adicionar novos blocos
        if check == 'N': #Caso não
            break # se o valor for N, ele sai do loop e imprime os blocos já adicionados

    check = str(input("\nDeseja alterar a blockchain? (S/N): ")) #Confere se quer fazer um teste na blockchain
    if check == 'S': 
        nBlock = int(input("\nQual o bloco?: ")) #Qual o bloco a ser modificados
        mblock = blockchain.chain[nBlock] = str(input("\nDigite os novos dados: ")) #Recebe os novos dados

    check = str(input("\nDeseja verificar a integridade da blockchain? (S/N): ")) #Faz um teste de integridade na blockchain
    if check == 'S':
        if blockchain.is_chain_valid() == True: #Caso passe no teste...
            print("\nA blockchain foi testada e validada!") #Avisa o usuário
        else: #Ou ao contrário
            print("A blockchain não foi validada!")

    check = str(input("\nDeseja visualizar a blockchain? (S/N): "))  #Verifica se quer visualizar a blockchain toda
    if check == 'S':
        response = {'chain': blockchain.chain, 'length': len(blockchain.chain)} #Estrutura os dados
        print('Chain: ') #Mostra os blocos
        for c1 in response['chain']:
            print(c1)
        print('Tamanho da Blockchain: ' + str(response['length'])) #Mostra o tamanho da corrente
    
