#include "palabras_random.h"
#include <stdlib.h>
#include <time.h>

static const char *DICCIONARIO[] = {
    
    "abeja", "abrir", "acabo", "acaso", "acero", "acosa", "actor", "aguda",
    "aguja", "ahora", "aires", "ajeno", "alado", "alamo", "alero", "alijo",
    "almas", "altar", "amado", "amiga", "amigo", "ancla", "angel", "anima",
    "ansia", "antes", "antro", "apaga", "apodo", "apoyo", "arder", "ardor",
    "arena", "armar", "armas", "arras", "artes", "asado", "asilo", "asomo",
    "astro", "atajo", "atril", "autor", "avaro", "avion", "ayuda", "azote",

    "banca", "banco", "barco", "barro", "beber", "belga", "bella", "bello",
    "besar", "bicho", "blusa", "bocas", "bolsa", "bomba", "bordo", "bosco",
    "brazo", "breve", "brida", "brisa", "broca", "bruma", "bueno", "bufon",
    "burla", "burro", "busca",

    "cabal", "caber", "cable", "cacao", "caida", "cajon", "calco", "caldo",
    "calma", "calor", "calvo", "campo", "canal", "canon", "canto", "capaz",
    "cargo", "carne", "carta", "casar", "casco", "cauce", "causa", "cavar",
    "cazar", "celda", "cerdo", "cerro", "chico", "chivo", "cielo", "cifra",
    "cinco", "cinta", "circo", "citar", "claro", "clavo", "cobro", "cocer",
    "cocos", "coima", "colmo", "color", "combo", "comer", "coral", "corte",
    "corto", "coser", "costo", "creta", "cruda", "crudo", "cruza", "cuaco",
    "cuajo", "cuero", "culpa", "culto", "curva",

    "danza", "datos", "debil", "debut", "decir", "dedos", "dejar", "delta",
    "deseo", "dicha", "dicho", "disco", "dobla", "doble", "dolor", "domar",
    "donde", "dosel", "drama", "droga", "dudar", "duelo", "dueno", "durar",

    "echar", "edema", "efebo", "egida", "elote", "enero", "entre", "envio",
    "erizo", "error", "espia", "estar", "extra",

    "fabla", "fajin", "falso", "falta", "fango", "favor", "fecal", "feliz",
    "feria", "ferro", "fibra", "fideo", "fiero", "fijar", "finca", "firme",
    "fisco", "fobia", "folio", "fondo", "forja", "forma", "forro", "frase",
    "freno", "fruta", "fuego", "fumar", "funda", "furia", "fusil",

    "gafas", "gamba", "ganas", "garbo", "garza", "gasto", "gateo", "genio",
    "gente", "girar", "globo", "golfo", "golpe", "gordo", "gorra", "gozar",
    "graba", "grana", "grasa", "grava", "gripe", "grupo", "guapo", "guiar",
    "guion", "guiso", "gusto",

    "haber", "hacer", "hacia", "hacha", "hampa", "harta", "hasta", "helar",
    "herir", "hielo", "hijos", "hogar", "honda", "honor", "horca", "hotel",
    "hueso", "humor",

    "icono", "ideal", "idolo", "igual", "impar", "indio", "intro",

    "jalar", "jarro", "jaula", "jefes", "jiron", "joker", "juego", "jugar",
    "junto", "jurar", "juzga",

    "karma",

    "labio", "lacra", "largo", "laser", "latir", "laudo", "lazos", "leche",
    "lecho", "legal", "lejos", "lento", "letra", "libra", "libro", "ligar",
    "limon", "lince", "linea", "lirio", "listo", "llano", "llena", "lleno",
    "logra", "logro", "lucha", "lugar", "lujos", "lunar",

    "madre", "mafia", "magia", "mango", "manos", "marco", "matiz", "mayor",
    "media", "medio", "mejor", "melon", "menos", "mente", "metro", "micro",
    "miedo", "mimar", "minas", "mirar", "misma", "mismo", "modos", "mojar",
    "molde", "monja", "monos", "moral", "morar", "morbo", "morir", "motor",
    "mover", "movil", "mozos", "mucho", "mundo", "musgo",

    "nacer", "nadie", "narco", "nardo", "negro", "noche", "norma", "norte",
    "notas", "novio", "nuevo", "nueve",

    "obeso", "obrar", "ocaso", "ocupa", "odiar", "oidos", "olivo", "opera",
    "optar", "orden", "oruga", "osada", "ovalo", "oveja", "ovulo",

    "padre", "pagar", "parda", "pared", "parte", "pasar", "paseo", "pasta",
    "patio", "pausa", "pecar", "pedal", "pegar", "pelar", "penas", "perla",
    "perro", "pesca", "piano", "picar", "picor", "pinza", "pista", "pixel",
    "plana", "plata", "plato", "plaza", "plomo", "pluma", "poder", "pollo",
    "pompa", "poner", "porta", "posar", "poste", "prado", "primo", "prisa",
    "prosa", "pubis", "pulpo", "punto",

    "queja", "quema",

    "radar", "rajar", "rampa", "rango", "rapto", "rasca", "rasgo", "razon",
    "recio", "regia", "regio", "reino", "reloj", "renta", "resto", "retro",
    "rezar", "riada", "rival", "robot", "rocio", "rodeo", "ronda", "rubro",
    "rugby", "ruido", "rumbo", "rural",

    "saber", "sacar", "salir", "salsa", "salto", "salud", "salvo", "samba",
    "sauna", "selva", "serio", "sigma", "signo", "silbo", "sobre", "socia",
    "socio", "solar", "solaz", "soler", "sopor", "sonar", "sorbo", "subir",
    "sucia", "sucio", "suelo", "sumar", "super", "surco", "sutil",

    "tabla", "tacos", "talar", "tanto", "tarda", "tarde", "tarea", "tarot",
    "tecla", "techo", "tejon", "telas", "temor", "tenor", "terca", "texto",
    "tibia", "timon", "tiras", "tomar", "torso", "total", "totem", "traer",
    "trama", "trapo", "traza", "trece", "treta", "tribu", "trigo", "trino",
    "tripa", "trozo", "truco", "turco", "tutor",

    "ultra", "umbra", "union", "unica", "unico", "urdir", "usura",

    "vacio", "vapor", "vasco", "veloz", "venas", "verde", "verso", "viaje",
    "vibra", "viejo", "vigor", "virus", "visor", "vista", "vivir", "vocal",
    "vodka", "volar", "votar", "vuelo",

    "yarda", "yermo",

    "zafar", "zafio", "zambo", "zarpa", "zombi", "zorra", "zurdo",
};

#define TOTAL (sizeof(DICCIONARIO) / sizeof(DICCIONARIO[0]))

const char *palabra_random(void)
{
    static int init = 0;
    if (!init) {
        srand((unsigned int)time(NULL));
        init = 1;
    }
    return DICCIONARIO[rand() % TOTAL];
}