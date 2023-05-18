## Implementações de Laboratório de Desenvolvimento I

#### Este é um repositório com implementações, no carater de exemplo, para os experimento e atividade da disiciplina de Laboratório de Desenvolvimento I do [IFSP, campus Catanduva](https://ctd.ifsp.edu.br/). 

![GitHub watchers](https://img.shields.io/github/watchers/flaviol-souza/lab-dev?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/flaviol-souza/lab-dev)
![Twitter Follow](https://img.shields.io/twitter/follow/flaviolsouza?style=social)

## Build With
Para a execução das implementações utilize: 
* seu IDE de preferência (sugestão VS Code)
* Python 3 (3.8.8 versão mínima)
```bash
pip install Flask
pip install pytest
pip install psycopg2
pip install sqlalchemy
pip install flask-restx
pip install python-dotenv
```

Se for utilizar Docker:
```bash
docker pull postgres:14.2
docker run -itd -e POSTGRES_USER=root -e POSTGRES_PASSWORD=ifsp -e POSTGRES_DB=<NAME_DB> -p 5432:5432 -v data:/var/lib/postgresql/data --name postgres_aula_8 postgres:14.2
```

## Run the project
Ao executar o script o servidor iniciara e informará a porta na qual a aplicação esta disponível.
```bash
python <YOUR_SCRIPT_PY>
```

## Implementations Lab. Dev.
* Aula 1: HTML, CSS and JS review.
* Aula 2: Hello World Flask and URL
* Aula 3: HTTP Methods review
* Aula 4: CRUD Restful
* Aula 5: Tratamento de erros e status HTTP
* Aula 6: Upload e Download de arquivos
* Aula 7: Refactoring service
* Aula 8: Conexão e Persistências de dados (Postgres)
* Aula 9: Integration Test