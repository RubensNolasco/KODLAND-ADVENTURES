**Kodland Adventures — README de Instalação e Funcionamento**

**Visão Geral**:
- **Descrição**: Projeto de jogo em Python usando Pygame Zero. O arquivo principal é `kodland_adventures.py`.
- **Pasta de assets**: imagens em `images/` e sons em `sounds/`. O arquivo `images/metadata.json` contém metadados relacionados às imagens.

**Requisitos**:
- **Python**: Python 3.8 ou superior instalado.
- **Bibliotecas**: `pygame` e `pgzero` (Pygame Zero).

**Instalação (Windows PowerShell)**:
- **Crie e ative um ambiente virtual** (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

- **Atualize pip e instale dependências**:

```powershell
python -m pip install --upgrade pip
pip install pygame pgzero
```

- **(opcional)**: se você preferir usar um `requirements.txt`, crie-o com as dependências `pygame` e `pgzero` e rode `pip install -r requirements.txt`.

**Executando o jogo**:
- **Opção 1 (recomendada)**: executar com `pgzrun`:

```powershell
pgzrun kodland_adventures.py
```

- **Opção 2**: executar diretamente (o arquivo chama `pgzrun.go()` no final):

```powershell
python kodland_adventures.py
```

- **Observação**: se obtiver erro `No module named pgzrun` instale `pgzero` conforme mostrado acima.

**Como Jogar / Controles**:
- **Mover**: tecla `←` (esquerda) e `→` (direita).
- **Pular**: tecla `Space`.
- **Abrir menu/confirmar saída**: `Esc`.
- **Alternar modo debug**: `F3` (mostra colisões/tiles quando ativo).
- **Mouse**: usado para clicar nos botões do menu (iniciar, sair, toggles de som, confirmar tutorial, reiniciar ao perder/ganhar).

**Regras básicas**:
- Colete as `Kodcoins` espalhadas pelo mapa. Ao coletar 22 moedas, você vence.
- Evite inimigos; pular sobre um inimigo mata-o. Tomar dano reduz sua vida (corações no canto superior esquerdo).

**Estrutura do projeto**:
- **`kodland_adventures.py`**: código principal do jogo.
- **`images/`**: sprites e imagens usadas (nomes precisam corresponder aos usados em `kodland_adventures.py`).
- **`images/metadata.json`**: metadados sobre as imagens (frames, atlas, etc.).
- **`sounds/`**: efeitos sonoros e trilha (`coin_sound`, `click`, `music_background`, ...).
- **`LICENSE`**: arquivo de licença do projeto.

**Boas práticas com assets**:
- **Nomes**: não altere os nomes dos arquivos em `images/` e `sounds/`, pois o código referencia nomes específicos (ex.: `idle_breathing (1)`, `coin_1`, `music_background`).
- **Adicionar animações**: siga o padrão de nome usado no código (`nome (1)`, `nome (2)`, ...).

**Resolução de problemas**:
- **Erro: No module named pgzrun**: execute `pip install pgzero` no ambiente ativo.
- **Problemas de áudio**: verifique se os arquivos em `sounds/` estão em formatos suportados (ex.: `.wav`, `.ogg`) e se o volume do sistema não está mudo.
- **Janela não abre / tela preta**: tente executar em outra versão do Python (3.8+), ou verifique se `pygame` está corretamente instalado.
- **Imagens não aparecem / sintomas de arquivo faltando**: verifique `images/metadata.json` e confirme que os arquivos referenciados existem.

**Desenvolvimento e testes**:
- **Editar o código**: abra `kodland_adventures.py` e modifique as constantes `WIDTH`, `HEIGHT`, `TILE_SIZE` ou `tilemap` conforme necessidade.
- **Reset do jogo**: o menu principal tem botão para reiniciar; também é feito programaticamente por `reset_game()`.

**Licença e Créditos**:
- Consulte o arquivo `LICENSE` na raiz do projeto para os termos de uso.
- **Créditos**: código principal em `kodland_adventures.py`. Assets organizados em `images/` e `sounds/`.

**Quer ajuda adicional?**
- Se quiser, eu posso: gerar um `requirements.txt`, adicionar scripts de execução (PowerShell) ou ajustar instruções específicas para distribuição.

***Fim do README***
