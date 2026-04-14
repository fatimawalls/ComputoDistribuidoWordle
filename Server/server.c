#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>

#define PORT 5000
#define MAX_ATTEMPTS 6
#define WORD_LEN 5

// ---------- DEBUG SEND ----------
void send_msg(int sock, const char *msg) {
    printf("📤 SERVER -> CLIENT: %s", msg);
    send(sock, msg, strlen(msg), 0);
}

// ---------- UTIL ----------
void trim_newline(char *str) {
    str[strcspn(str, "\r\n")] = 0;
}

// ---------- USUARIOS ----------
int usuario_existe(const char *user) {
    FILE *f = fopen("usuarios.txt", "r");
    if (!f) return 0;

    char line[200];

    while (fgets(line, sizeof(line), f)) {
        char u[100], p[100], w[100];
        sscanf(line, "%[^|]|%[^|]|%[^\n]", u, p, w);

        if (strcmp(u, user) == 0) {
            fclose(f);
            return 1;
        }
    }

    fclose(f);
    return 0;
}

int validar_usuario(const char *user, const char *pass, char *wins_out) {
    FILE *f = fopen("usuarios.txt", "r");
    if (!f) return 0;

    char line[200];

    while (fgets(line, sizeof(line), f)) {
        char u[100], p[100], w[100];
        sscanf(line, "%[^|]|%[^|]|%[^\n]", u, p, w);

        if (strcmp(u, user) == 0 && strcmp(p, pass) == 0) {
            strcpy(wins_out, w);
            fclose(f);
            return 1;
        }
    }

    fclose(f);
    return 0;
}

void registrar_usuario(const char *user, const char *pass) {
    FILE *f = fopen("usuarios.txt", "a");
    if (!f) return;

    fprintf(f, "%s|%s|-\n", user, pass);
    fclose(f);
}

void agregar_victoria(const char *user) {
    FILE *f = fopen("usuarios.txt", "r");
    FILE *temp = fopen("temp.txt", "w");

    char line[200];

    while (fgets(line, sizeof(line), f)) {
        char u[100], p[100], w[100];
        sscanf(line, "%[^|]|%[^|]|%[^\n]", u, p, w);

        if (strcmp(u, user) == 0) {
            strcat(w, ".");
        }

        fprintf(temp, "%s|%s|%s\n", u, p, w);
    }

    fclose(f);
    fclose(temp);
    remove("usuarios.txt");
    rename("temp.txt", "usuarios.txt");
}

// ---------- WORDLE ----------
char* generar_palabra() {
    return "perro";
}

void evaluar(char *secreta, char *intento, char *resultado) {
    for (int i = 0; i < WORD_LEN; i++) {
        if (intento[i] == secreta[i]) resultado[i] = 'C';
        else if (strchr(secreta, intento[i])) resultado[i] = 'P';
        else resultado[i] = 'A';
    }
    resultado[WORD_LEN] = '\0';
}

// ---------- PARTIDA ----------
void jugar_partida(int client_sock, char *usuario) {
    char buffer[1024];
    char resultado[WORD_LEN + 1];
    char *secreta = generar_palabra();

    int intentos = 0;

    send_msg(client_sock, "{\"type\":\"start\"}\n");

    while (intentos < MAX_ATTEMPTS) {
        memset(buffer, 0, sizeof(buffer));
        int bytes = recv(client_sock, buffer, sizeof(buffer)-1, 0);
        if (bytes <= 0) return;

        trim_newline(buffer);
        printf("📥 CLIENT -> SERVER: %s\n", buffer);

        char word[50];

        if (!strstr(buffer, "\"type\":\"guess\"") ||
            sscanf(buffer, "{\"type\":\"guess\",\"word\":\"%[^\"]\"}", word) != 1) {
            
            send_msg(client_sock, "{\"type\":\"error\",\"message\":\"formato\"}\n");
            continue;
        }

        if (strlen(word) != WORD_LEN) {
            send_msg(client_sock, "{\"type\":\"error\",\"message\":\"longitud\"}\n");
            continue;
        }

        evaluar(secreta, word, resultado);

        char msg[128];

        if (strcmp(word, secreta) == 0) {
            snprintf(msg, sizeof(msg),
                "{\"type\":\"result\",\"data\":\"%s\",\"status\":\"win\"}\n",
                resultado);
            send_msg(client_sock, msg);
            agregar_victoria(usuario);
            return;
        } else {
            snprintf(msg, sizeof(msg),
                "{\"type\":\"result\",\"data\":\"%s\",\"status\":\"continue\"}\n",
                resultado);
            send_msg(client_sock, msg);
        }

        intentos++;
    }

    send_msg(client_sock,
        "{\"type\":\"result\",\"data\":\"-----\",\"status\":\"lose\"}\n");
}

// ---------- CLIENTE ----------
void manejar_cliente(int client_sock) {
    char usuario[100];
    char buffer[1024];

    while (1) {
        memset(buffer, 0, sizeof(buffer));
        int bytes = recv(client_sock, buffer, sizeof(buffer)-1, 0);
        if (bytes <= 0) return;

        trim_newline(buffer);
        printf("📥 CLIENT -> SERVER: %s\n", buffer);

        char user[100], pass[100], wins[100];

        if (strstr(buffer, "\"type\":\"login\"") &&
            sscanf(buffer, "{\"type\":\"login\",\"user\":\"%[^\"]\",\"pass\":\"%[^\"]\"}", user, pass) == 2) {

            if (validar_usuario(user, pass, wins)) {
                strcpy(usuario, user);

                char msg[200];
                snprintf(msg, sizeof(msg),
                    "{\"type\":\"auth\",\"status\":\"ok\",\"wins\":\"%s\"}\n",
                    wins);

                send_msg(client_sock, msg);
                break;
            } else {
                send_msg(client_sock, "{\"type\":\"auth\",\"status\":\"error\"}\n");
            }
        }

        else if (strstr(buffer, "\"type\":\"register\"") &&
            sscanf(buffer, "{\"type\":\"register\",\"user\":\"%[^\"]\",\"pass\":\"%[^\"]\"}", user, pass) == 2) {

            if (!usuario_existe(user)) {
                registrar_usuario(user, pass);
                strcpy(usuario, user);

                send_msg(client_sock,
                    "{\"type\":\"auth\",\"status\":\"ok\",\"wins\":\"-\"}\n");
                break;
            } else {
                send_msg(client_sock, "{\"type\":\"auth\",\"status\":\"error\"}\n");
            }
        }

        else {
            send_msg(client_sock, "{\"type\":\"error\",\"message\":\"formato\"}\n");
        }
    }

    while (1) {
        jugar_partida(client_sock, usuario);

        send_msg(client_sock, "{\"type\":\"play_again\"}\n");

        memset(buffer, 0, sizeof(buffer));
        int bytes = recv(client_sock, buffer, sizeof(buffer)-1, 0);
        if (bytes <= 0) break;

        trim_newline(buffer);
        printf("📥 CLIENT -> SERVER: %s\n", buffer);

        char val[10];

        if (strstr(buffer, "\"type\":\"play_again\"") &&
            sscanf(buffer, "{\"type\":\"play_again\",\"value\":\"%[^\"]\"}", val) == 1) {

            if (strcmp(val, "SI") != 0) break;
        } else {
            break;
        }
    }

    close(client_sock);
    exit(0);
}

// ---------- MAIN ----------
int main() {
    int server_fd, client_sock;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);

    signal(SIGCHLD, SIG_IGN);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 5);

    printf("🔥 Servidor FULL corriendo en puerto %d...\n", PORT);

    while (1) {
        client_sock = accept(server_fd, (struct sockaddr *)&address, &addrlen);

        printf("🟢 Nuevo cliente conectado\n");

        if (fork() == 0) {
            close(server_fd);
            manejar_cliente(client_sock);
        }

        close(client_sock);
    }

    return 0;
}