using Microsoft.AspNetCore.Mvc;
using methods.Model;

namespace methods.Controllers;

[ApiController]
[Route("api/imdbs")]
public class ImdbController : ControllerBase
{
    private static int countId = 1;
    private static List<Imdb> movies = new List<Imdb>();

    [HttpGet]
    public ActionResult<List<Imdb>> GetAll(int limit, bool top){
        if(movies == null || !movies.Any()){
            return StatusCode(200, "Não existem filmes cadastrados");
        }
        var getMovies = movies;
        if(top){
           getMovies = getMovies.OrderBy(m => m.Nota).ToList(); 
        }
        if(limit > 0){
            getMovies = getMovies.Take(limit).ToList();
        }
        return Ok(getMovies);        
    }

    [HttpGet("{id}")]
    public ActionResult<Imdb> GetImdb(int id){
        Imdb imdb;
        try
        {
            imdb = getImdbById(id);
        }
        catch (System.Exception)
        {
            return StatusCode(500, "A plataforma não esta preparada para essa chamada!");
        }
        if(imdb == null){
            return NotFound("IMDB não existe!"); // Retorna Http Status 404 
        }
        return Ok(imdb);
    }

    [HttpDelete("{id}")]
    public ActionResult<bool> DeleteImdb(int id){
        Imdb imdb = getImdbById(id);
        foreach(Imdb i in movies){
            if(i.Id == id){
                imdb = i;
                break;
            }
        }
        if(imdb != null){
            movies.Remove(imdb);
            return true;
        }
        return false;
    }

    [HttpPost]
    public ActionResult<bool> CreateImdb(Imdb imdb){
        if(imdb == null){
            return StatusCode(204, "Valores inválidos!");
        } else if(imdb.Titulo == null || imdb.Titulo == "" || imdb.AnoLancamento < 1800){
            return StatusCode(204, "É necessário informar Titulo e Ano de Lançamento do Filme.");
        }

        imdb.Id = countId++;
        movies.Add(imdb);
        return Ok(true);
    }

    [HttpPut("{id}")]
    public ActionResult<bool> updateImdb(int id, Imdb imdb){
        Imdb imdbOld = getImdbById(id);
        if(imdbOld == null){
            return StatusCode(404, "Filme não encontrado");
        }
        if(imdb == null){
            return StatusCode(204, "Parâmetro inválido.");
        } else if(imdb.Titulo == null || imdb.Titulo == "" || imdb.AnoLancamento < 1800){
            return StatusCode(204, "É necessário informar Titulo e Ano de Lançamento do Filme.");
        }
        if(imdb.AnoLancamento > 0){
            imdbOld.AnoLancamento = imdb.AnoLancamento;
        }
        if(imdb.Titulo != null){
            imdbOld.Titulo = imdb.Titulo;
        }
        return Ok(true);
    }
    
    [HttpPatch("{id}/voto/{nota}")]
    public ActionResult<bool> voteImdb(int id, double nota){
        Imdb imdb = getImdbById(id);
        if(imdb == null){
            return StatusCode(404, "Filme não encontrado");
        }
        if(nota < 0 || nota > 10){
            return StatusCode(400, "A nota é inválida.");
        }
        imdb.Notas.Add(nota);
        return Ok(true);
    }

    private Imdb getImdbById(int id){
        foreach(Imdb i in movies){
            if(i.Id == id){
                return i;
            }
        }
        return null;
    }
}