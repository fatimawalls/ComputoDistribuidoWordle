#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_USERS 100
#define MAX_WORDS 100

typedef struct {
    char user[50];
    char pass[50];
    int wins;
    char words[MAX_WORDS][20];
    int word_count;
} Usuario;

Usuario usuarios[MAX_USERS];
int total_usuarios = 0;

void cargar_usuarios() {

    FILE *f = fopen("usuarios.json", "r");
    if (!f) {
        total_usuarios = 0;
        return;
    }

    char line[512];
    Usuario u;
    total_usuarios = 0;

    int dentro_objeto = 0;

    while (fgets(line, sizeof(line), f)) {

        // inicio de objeto
        if (strchr(line, '{')) {
            memset(&u, 0, sizeof(Usuario));
            u.word_count = 0;
            dentro_objeto = 1;
        }

        if (!dentro_objeto) continue;

        // user
        if (strstr(line, "\"user\"")) {
            sscanf(line, " \"user\": \"%[^\"]\"", u.user);
        }

        // pass
        if (strstr(line, "\"pass\"")) {
            sscanf(line, " \"pass\": \"%[^\"]\"", u.pass);
        }

        // wins
        if (strstr(line, "\"wins\"")) {
            sscanf(line, " \"wins\": %d", &u.wins);
        }

        // words
        if (strstr(line, "\"words\"")) {

            char *start = strchr(line, '[');
            char *end = strchr(line, ']');

            if (start && end) {
                char temp[300] = {0};
                strncpy(temp, start + 1, end - start - 1);

                char *token = strtok(temp, ",");

                while (token) {
                    sscanf(token, " \"%[^\"]\"", u.words[u.word_count]);
                    u.word_count++;
                    token = strtok(NULL, ",");
                }
            }
        }

        // fin de objeto
        if (strchr(line, '}')) {

            // 🔥 SOLO guardar si es válido
            if (strlen(u.user) > 0 && strlen(u.pass) > 0) {
                usuarios[total_usuarios++] = u;
            } else {
                printf("⚠️ Usuario ignorado por datos inválidos\n");
            }

            dentro_objeto = 0;
        }
    }

    fclose(f);

    printf("📦 Usuarios cargados: %d\n", total_usuarios);
}
void guardar_usuarios() {
    FILE *f = fopen("usuarios.json", "w");

    fprintf(f, "[\n");

    for (int i = 0; i < total_usuarios; i++) {
        Usuario u = usuarios[i];

        fprintf(f, "  {\n");
        fprintf(f, "    \"user\": \"%s\",\n", u.user);
        fprintf(f, "    \"pass\": \"%s\",\n", u.pass);
        fprintf(f, "    \"wins\": %d,\n", u.wins);

        fprintf(f, "    \"words\": [");

        for (int j = 0; j < u.word_count; j++) {
            fprintf(f, "\"%s\"", u.words[j]);
            if (j < u.word_count - 1) fprintf(f, ",");
        }

        fprintf(f, "]\n");

        if (i < total_usuarios - 1)
            fprintf(f, "  },\n");
        else
            fprintf(f, "  }\n");
    }

    fprintf(f, "]\n");
    fclose(f);
}
int usuario_existe(const char *user) {
    cargar_usuarios();

    for (int i = 0; i < total_usuarios; i++) {
        if (strcmp(usuarios[i].user, user) == 0)
            return 1;
    }
    return 0;
}

int validar_usuario(const char *user, const char *pass, int *wins) {
    cargar_usuarios();

    for (int i = 0; i < total_usuarios; i++) {
        if (strcmp(usuarios[i].user, user) == 0 &&
            strcmp(usuarios[i].pass, pass) == 0) {

            *wins = usuarios[i].wins;
            return 1;
        }
    }
    return 0;
}

void registrar_usuario(const char *user, const char *pass) {
    cargar_usuarios();

    Usuario u = {0};
    strcpy(u.user, user);
    strcpy(u.pass, pass);
    u.wins = 0;
    u.word_count = 0;

    usuarios[total_usuarios++] = u;

    guardar_usuarios();
}

void agregar_victoria(const char *user) {
    cargar_usuarios();

    for (int i = 0; i < total_usuarios; i++) {
        if (strcmp(usuarios[i].user, user) == 0) {
            usuarios[i].wins++;
        }
    }

    guardar_usuarios();
}

void obtener_palabras_usuario(const char *user, char words[][20], int *count) {
    cargar_usuarios();

    for (int i = 0; i < total_usuarios; i++) {
        if (strcmp(usuarios[i].user, user) == 0) {

            *count = usuarios[i].word_count;

            for (int j = 0; j < *count; j++) {
                strcpy(words[j], usuarios[i].words[j]);
            }
        }
    }
}

int palabra_ya_resuelta(char words[][20], int count, const char *palabra) {
    for (int i = 0; i < count; i++) {
        if (strcmp(words[i], palabra) == 0)
            return 1;
    }
    return 0;
}

void agregar_palabra_usuario(const char *user, const char *palabra) {
    cargar_usuarios();

    for (int i = 0; i < total_usuarios; i++) {
        if (strcmp(usuarios[i].user, user) == 0) {

            if (!palabra_ya_resuelta(usuarios[i].words,
                                     usuarios[i].word_count,
                                     palabra)) {

                strcpy(usuarios[i].words[usuarios[i].word_count++], palabra);
            }
        }
    }

    guardar_usuarios();
}
