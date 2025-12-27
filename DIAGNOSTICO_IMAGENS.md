# 🔍 Diagnóstico: Imagens Não Estão Funcionando

## ✅ Correções Aplicadas

1. **Caminhos corrigidos:** Agora usa caminhos absolutos ao invés de relativos
2. **Rota de servir arquivos:** Simplificada e corrigida
3. **Pastas criadas automaticamente:** `source/static/uploads/` e subpastas

## 🔍 Como Testar

### 1. **Testar Upload de Imagem**

Faça um POST para criar uma pelada com logo:
```bash
POST http://192.168.18.38:5001/api/peladas/
Content-Type: multipart/form-data

nome: "Teste"
cidade: "São Paulo"
logo: [arquivo]
```

### 2. **Verificar se a Imagem foi Salva**

A imagem deve estar em:
```
C:\Users\iagoa\Desktop\efootbool\source\static\uploads\peladas\logo_YYYYMMDD_HHMMSS_XXXXXX.jpg
```

### 3. **Testar Acesso à Imagem**

No navegador ou celular, acesse:
```
http://192.168.18.38:5001/static/uploads/peladas/logo_YYYYMMDD_HHMMSS_XXXXXX.jpg
```

**Deve mostrar a imagem!**

---

## 🐛 Problemas Comuns

### Problema 1: "404 Not Found" ao acessar imagem

**Causa:** Caminho da imagem está errado ou arquivo não existe

**Solução:**
1. Verifique se o arquivo foi salvo na pasta correta
2. Verifique se a URL está correta (deve começar com `/static/uploads/`)
3. Verifique se o servidor está rodando

### Problema 2: "CORS error" ao carregar imagem

**Causa:** CORS não está configurado para servir arquivos estáticos

**Solução:** Já está configurado! O CORS aceita qualquer origem em desenvolvimento.

### Problema 3: Imagem não aparece no frontend

**Causa:** URL da imagem está incorreta ou relativa

**Solução:**
- Use URL completa: `http://192.168.18.38:5001/static/uploads/...`
- Não use URL relativa se estiver em outro dispositivo

---

## 📝 Checklist de Verificação

- [ ] Servidor está rodando em `0.0.0.0:5001`
- [ ] Firewall permite conexões na porta 5001
- [ ] Pasta `source/static/uploads/` existe
- [ ] Upload de imagem retorna `logo_url` ou `foto_url` ou `escudo_url`
- [ ] URL da imagem começa com `/static/uploads/`
- [ ] Acessando a URL completa no navegador mostra a imagem

---

## 🔧 Comandos Úteis

### Verificar se arquivo existe:
```powershell
Test-Path "C:\Users\iagoa\Desktop\efootbool\source\static\uploads\peladas\*.jpg"
```

### Listar arquivos salvos:
```powershell
Get-ChildItem "C:\Users\iagoa\Desktop\efootbool\source\static\uploads" -Recurse
```

### Verificar se servidor está escutando:
```powershell
netstat -ano | findstr :5001
```

---

## 💡 Dica: URLs Completas no Frontend

No frontend, ao exibir imagens, use URLs completas:

```javascript
// ✅ CORRETO
const imageUrl = `http://192.168.18.38:5001${pelada.logo_url}`;

// ❌ ERRADO - não funciona em outro dispositivo
const imageUrl = pelada.logo_url;
```

Ou configure uma variável de ambiente:
```javascript
const API_BASE_URL = 'http://192.168.18.38:5001';
const imageUrl = `${API_BASE_URL}${pelada.logo_url}`;
```

