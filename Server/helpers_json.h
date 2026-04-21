#ifndef HELPERS_JSON_H
#define HELPERS_JSON_H

int usuario_existe(const char *user);
int validar_usuario(const char *user, const char *pass, int *wins);
void registrar_usuario(const char *user, const char *pass);
void agregar_victoria(const char *user);

void obtener_palabras_usuario(const char *user, char words[][20], int *count);
int palabra_ya_resuelta(char words[][20], int count, const char *palabra);
void agregar_palabra_usuario(const char *user, const char *palabra);

#endif
