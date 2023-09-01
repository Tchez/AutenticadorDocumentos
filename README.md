<h1>Autenticador de Documentos</h1>

### Esse projeto é uma aplicação WEB criada para a AP1 da disciplina de Segurança de Sistemas, onde a atividade consiste em desenvolver um assinador de documentos digitais utilizando criptografia de chave assimétrica e funções hash criptográficas.

## Principais funcionalidades:

- Autenticação de usuário;
- Geração de par de chaves assimétricas para o usuário;
- Salvar documento no sistema;
- Assinar documento usando chave privada do usuário;
- Visualizar lista de documentos assinados pelo usuário;
- Visualizar um documento assinado pelo usuário;
- Checar se o documento foi assinado no sistema pelo usuário;

## Como rodar a aplicação:

Crie e habilite um ambiente virtual

```console
  python -m venv venv
```

```console
  venv\Scripts\activate | windows
  .venv/bin/activate | linux e macOs
```

Instale as dependências do projeto

```console
  pip install -r requirements.txt
```

## Uso

Passe os modelos para o banco de dados:

```console
python manage.py makemigrations
```

```console
python manage.py migrate
```

Rode o servidor:

```console
python manage.py runserver 8000
```

O servidor estará disponível em:

```console
http://127.0.0.1:8000/
```
