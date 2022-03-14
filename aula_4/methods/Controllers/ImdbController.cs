using Microsoft.AspNetCore.Mvc;
using methods.Model;

namespace methods.Controllers;

[ApiController]
[Route("[controller]")]
public class ImdbController : ControllerBase
{
    List<Imdb> movies;
    private readonly ILogger<ImdbController> _logger;

    public ImdbController(ILogger<ImdbController> logger)
    {
        _logger = logger;
        movies = new List<Imdb>();
    }

    public Imdb initImdb(){
        Imdb imdb = new Imdb();
        imdb.Id = 1;
        imdb.Titulo = "The Batman";
        imdb.AnoLancamento = 2022;
        imdb.Nota = 8.4;
        return imdb;
    }

    [Route("top-movies")]
    [HttpGet(Name = "GetImdbTop")]
    public List<Imdb> Get()
    {
        if(!movies.Any()){
            movies.Add(initImdb());
        }
        
        return movies;
    }

}