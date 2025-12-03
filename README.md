

Esse projeto é um trabalho de Redes onde a gente precisa criar um **cliente**, um **proxy** e um **servidor**, e observar como o tráfego se comporta quando a rede está boa, ruim, com delay, perda, etc.  
Então aqui eu vou explicar de forma simples como tudo funciona e como qualquer pessoa pode rodar.

---

## 🟦 Como o sistema funciona 

A ideia geral é:

```
CLIENTE → PROXY → SERVIDOR
```

O cliente não fala direto com o servidor.  
Ele passa pelo proxy, que fica no meio medindo tudo o que acontece.

O proxy coleta várias métricas, tipo:

- RTT (tempo de ida e volta)
- RTTVar (variação do RTT)
- Throughput (velocidade da transferência)
- Goodput (o que realmente chegou útil)
- Retransmissões (estimadas)
- Tamanho da janela de congestão (cwnd)

Além disso, o proxy usa umas “otimizações” tipo:

- Pacing → faz o envio mais suave, sem rajadas gigantes  
- Ajuste de Buffer → muda o tamanho do buffer dependendo do RTT real

O servidor só manda blocos grandes de dados (tipo 500 KB) para o cliente para a gente testar a performance.

---

## 🟧 O que cada arquivo faz

### 📌 **servidor.py**
O servidor recebe as conexões e toda vez que o cliente manda um “PING”, ele manda de volta um bloco de 500 KB.  
Serve pra gerar tráfego pesado pro proxy medir.

---

### 📌 **proxy.py**
Esse é o mais importante.  
Ele:

- Fica entre cliente e servidor
- Recebe os dados de um e repassa pro outro
- Mede tudo (RTT, throughput, perda, etc)
- Salva as métricas num arquivo CSV dentro de uma pasta chamada `logs`
- Roda threads pra encaminhar os dados mais rápido
- Aplica pacing e ajuste de buffers

Toda vez que o proxy está rodando, ele gera arquivos do tipo:

```
logs/metricas
```

---

### 📌 **cliente.py**
O cliente conecta no proxy e manda várias requisições.  
Ele:

- Envia “PING”
- Espera receber 500 KB de volta
- Mede o RTT
- Imprime o resultado no terminal

A ideia é repetir isso várias vezes pra ver como a rede se comporta.

---

### 📌 **graficos.py**
Pega os CSVs que o proxy salvou e gera gráficos:

- RTT
- Throughput
- Goodput
- Retransmissões
- cwnd (janela de congestão)

Os gráficos ficam no mesmo diretório.

---

## 🟨 Como rodar o projeto 

Você precisa de 3 janelas do terminal.

---

### 1️⃣ Rodar o servidor

Abra o terminal na pasta do projeto e execute:

```
python servidor.py
```

Ele vai ficar escutando na porta 8080.

---

### 2️⃣ Rodar o proxy

Em outra janela:

```
python proxy.py
```

Quando ele iniciar, vai aparecer algo tipo:

```
Arquivo de métricas criado em logs/...
```

Isso significa que deu certo.

---

### 3️⃣ Rodar o cliente

Na terceira janela:

```
python cliente.py
```

Você vai ver algo assim:

```
[CLIENTE] Pacote 1: 500000 bytes, RTT = 45ms
[CLIENTE] Pacote 2: 500000 bytes, RTT = 120ms
```

E assim por diante.

---

## 🟩 Como simular problema na rede 

Esse programa é legal porque dá pra simular uma rede ruim usando o **Clumsy**.

Você pode colocar delay, perda de pacotes e limitar a banda.

### Exemplos que usei no trabalho:

- Rede normal → não ativa nada
- Delay 50ms + perda 1%
- Delay 100ms + perda 2%
- Banda limitada pra 5 Mbps

Quando você mudar isso, os valores de RTT do cliente vão subir, o throughput vai cair e os gráficos vão mudar.

---

## 🟦 Como ver os gráficos

Depois de rodar o cliente algumas vezes, execute:

```
python graficos.py
```

Os gráficos vão aparecer na pasta do projeto.

---

## 🟧 Conclusão

O programa inteiro serve pra ver como o TCP se comporta com:

- atraso
- perda
- gargalo de banda

Dá pra pegar os CSVs e os gráficos pra analisar tudinho direitinho, como o professor pediu no trabalho.

