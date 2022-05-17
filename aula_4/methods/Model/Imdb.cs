using System.Text.Json;
using System.Text.Json.Serialization;

namespace methods.Model;

public class Imdb {

    public Imdb(){
        Notas = new List<double>();
    }

    public Imdb(int id, String titulo, int ano) 
        : this() {        
        Id = id;
        Titulo = titulo;
        AnoLancamento = ano;        
    }
    
    public int Id {get; set;}
    public String? Titulo {get; set;}    
    public int AnoLancamento {get; set;}
    [JsonIgnore]
    public List<double>? Notas {get; set;}
    public double Nota => Notas.Any() ? Notas.Average() : 0.0;
}