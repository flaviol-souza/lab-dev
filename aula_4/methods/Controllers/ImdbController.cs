using Microsoft.AspNetCore.Mvc;
using methods.Model;

namespace methods.Controllers;

[ApiController]
[Route("[controller]")]
public class ImdbController : ControllerBase
{
    private static int countId = 1;
    private static List<Imdb> movies = new List<Imdb>();

    [HttpGet]
    public String Get(){
        return "Olá Mundo";
    }

    [HttpDelete("{id}")]
    public bool DeleteImdb(int id){
        Imdb aux = null;
        foreach(Imdb i in movies){
            if(i.Id == id){
                aux = i;
                break;
            }
        }
        if(aux != null){
            movies.Remove(aux);
            return true;
        }
        return false;
    }



    [HttpPost]
    public bool CreateImdb(Imdb imdb){
        imdb.Id = countId++;
        movies.Add(imdb);
        return true;
    }

    [HttpGet("{id}")]
    public Imdb GetImdb(int id){
        foreach(Imdb i in movies){
            if(i.Id == id){
                return i;
            }
        }

        return null;
    }

    [HttpGet("top")]
    public List<Imdb> GetAll(){
        if(!movies.Any()){
            movies.Add(initImdb());
        }
        return movies;
    }

     public Imdb initImdb(){
        Imdb imdb = new Imdb(countId++,  "The Batman", 2022);
        imdb.Nota = 8.4;
        return imdb;
    }
}