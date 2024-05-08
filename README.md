<h1>
    <a href="https://www.dio.me/">
     <img align="center" width="40px" src="https://hermes.digitalinnovation.one/assets/diome/logo-minimized.png"></a>
    <span> Python AI Backend Developer </span>
</h1>


# :computer: Desafio de projeto:

## Criando Uma API Com FastAPI Utilizando TDD

### Entendendo o Desafio

Essa aplicação tem como objetivo principal trazer conhecimentos sobre o TDD, na prática, desenvolvendo uma API com o Framework Python, FastAPI. Utilizando o banco de dados MongoDB, para validações o Pydantic, para os testes Pytest e entre outras bibliotecas.

Projeto instrutora:
https://github.com/digitalinnovationone/store_api

### Desafio Final
Create
Mapear uma exceção, caso dê algum erro de inserção e capturar na controller
Update
Modifique o método de patch para retornar uma exceção de Not Found, quando o dado não for encontrado
a exceção deve ser tratada na controller, pra ser retornada uma mensagem amigável pro usuário
ao alterar um dado, a data de updated_at deve corresponder ao time atual, permitir modificar updated_at também
Filtros
cadastre produtos com preços diferentes
aplique um filtro de preço, assim: (price > 5000 and price < 8000)

# :zap:  Tecnologias Utilizadas

- pipenv - controle de versão
- PostgreSQL - banco de dados com docker-compose
- SQLAlchemy + Pydantic + Alembic - conexão com banco de dados
- FastAPI - desenvolver a aplicação

# :bulb: Solução do desafio

https://medium.com/@cgrinaldi/a-simple-python-starter-project-c71b0e57b929
git init
pipenv run pre-commit install

O código foi feita seguindo a aula da instrutora.

Para executar o código:

- Rodar banco de dados na pasta workout_api

```console
$ docker-compose up -d
```

- Rodar alembic na pasta do projeto (local do Makefile)

```console
$ make run-migrations
```

- Rodar app na pasta do projeto

```console
$ make run
```

## Adicionar query parameters nos endpoints

      - atleta
            - nome
            - cpf

Foi adicionado no arquivo atleta/controller.py. É necessário fornecer nome e cpf para a consulta.

```python
@router.get(
        path='/nome={nome}',
        summary='consultar um atleta pelo nome',
        status_code = status.HTTP_200_OK,
        response_model= AtletaOut,
        )


async def query(nome: str, db_session: DatabaseDependency, cpf: str | None = None) -> AtletaOut:
    atleta: AtletaOut = (
    await db_session.execute(select(AtletaModel).filter_by(nome=nome, cpf=cpf))
        ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= f'Atleta não encontrado com nome: {nome}'
            )

    return atleta
```

## Customizar response de retorno de endpoints

      - get all
            - atleta
                  - nome
                  - centro_treinamento
                  - categoria

Foi criado o schema personalizado em atletas/schemas.py

```python
class AtletaResponse(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', example='Joao', max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do Atleta')]
```

Foi adicionado o endpoint no arquivo atleta/controller.py.

```python
@router.get(
        path='/all_atletas',
        summary='consulta personalizada todos os atletas',
        status_code = status.HTTP_200_OK,
        response_model= list[AtletaResponse],
        )


async def query(db_session: DatabaseDependency) -> list[AtletaResponse]:
    atletas: list[AtletaResponse] = (await db_session.execute(select(AtletaModel))).scalars().all()

    return [AtletaResponse.model_validate(atleta) for atleta in atletas]
```

## Manipular exceção de integridade dos dados em cada módulo/tabela

      - sqlalchemy.exc.IntegrityError e devolver a seguinte mensagem: “Já existe um atleta cadastrado com o cpf: x”
      - status_code: 303

No arquivo atleta/controller.py foi necessário importar:

```python
from sqlalchemy.exc import IntegrityError
```

E adicionada a exceção após o try commit.

```python
    await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
        )
```
Analogamente para o controller.py de categorias e centro_treinamento, mas ao invés do CPF o usei o Nome que é a variável única nesse caso.

## Adicionar paginação utilizando a lib: fastapi-pagination

      - limit e offset

No arquivo main.py adicionei o import:

```python
from fastapi_pagination import add_pagination
```
E ao final do arquivo adicionei:

```python
add_pagination(app)
```

Adicionei paginação para a consulta de todos os atletas modificando no arquivo atleta/controller.py

Import:

```python
#Add pagination with SQLAlchemy
from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.ext.sqlalchemy import paginate
```
Endpoint:

```python
@router.get(
        path='/',
        summary='consultar todos os atletas',
        status_code = status.HTTP_200_OK,
        response_model= LimitOffsetPage[AtletaOut],
        )


async def query(db_session: DatabaseDependency):

    return await paginate(db_session, select(AtletaModel))
```

Todos os endpoints estão funcionando como esperado.

<img src="endpoints.png" alt="Endpoints WorkoutApi" >
