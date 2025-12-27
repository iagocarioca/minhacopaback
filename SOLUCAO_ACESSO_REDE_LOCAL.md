# 🔧 Solução: Acesso à API via WiFi (Rede Local)

## ✅ Status Atual

- **Servidor configurado:** ✅ Escutando em `0.0.0.0:5001` (aceita conexões de qualquer interface)
- **IP da máquina na rede:** `192.168.18.38`
- **Porta:** `5001`

## 🔍 Problema Identificado

O servidor está correto, mas provavelmente:
1. **Firewall do Windows** está bloqueando a porta 5001
2. **Frontend está usando `localhost`** ao invés do IP da rede local

---

## 🛠️ Soluções

### 1. **Configurar o Frontend para usar o IP da Rede Local**

No seu frontend, ao invés de:
```javascript
// ❌ ERRADO - só funciona no mesmo computador
const API_URL = 'http://localhost:5001/api'
// ou
const API_URL = 'http://127.0.0.1:5001/api'
```

Use:
```javascript
// ✅ CORRETO - funciona na rede local
const API_URL = 'http://192.168.18.38:5001/api'
```

**Nota:** Se o IP mudar (conexão WiFi diferente), você precisará atualizar.

---

### 2. **Liberar Porta 5001 no Firewall do Windows**

#### Opção A: Via Interface Gráfica

1. Abra o **Windows Defender Firewall**
2. Clique em **Configurações Avançadas**
3. Clique em **Regras de Entrada** (Inbound Rules)
4. Clique em **Nova Regra...**
5. Selecione **Porta** → Próximo
6. Selecione **TCP** e digite `5001` → Próximo
7. Selecione **Permitir a conexão** → Próximo
8. Marque todas as opções (Domínio, Privada, Pública) → Próximo
9. Dê um nome: "Flask API Port 5001" → Concluir

#### Opção B: Via PowerShell (Administrador)

```powershell
New-NetFirewallRule -DisplayName "Flask API Port 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

---

### 3. **Verificar se o Servidor está Acessível**

No celular (conectado na mesma WiFi), abra o navegador e teste:

```
http://192.168.18.38:5001/
```

Deve retornar:
```json
{"message": "XClickPayEx API"}
```

Se não funcionar, o firewall está bloqueando.

---

### 4. **Verificar CORS (já está configurado, mas confirme)**

O CORS já está configurado para aceitar requisições de qualquer origem na rede local. Se precisar adicionar o IP específico do celular, edite `source/__init__.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3004",
            "http://192.168.18.*"  # Aceita qualquer IP da rede 192.168.18.x
        ],
        ...
    }
})
```

---

## 📱 Teste Rápido no Celular

1. **Conecte o celular na mesma rede WiFi**
2. **No navegador do celular, acesse:**
   ```
   http://192.168.18.38:5001/
   ```
3. **Se aparecer `{"message": "XClickPayEx API"}`, está funcionando!**
4. **Agora configure o frontend para usar:**
   ```
   http://192.168.18.38:5001/api
   ```

---

## 🔄 Se o IP Mudar

Se você conectar em outra rede WiFi, o IP pode mudar. Para descobrir o novo IP:

**Windows:**
```cmd
ipconfig | findstr IPv4
```

**Ou no PowerShell:**
```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}
```

---

## ⚠️ Troubleshooting

### Problema: "Connection refused" ou timeout
- ✅ Verifique se o firewall está liberado (passo 2)
- ✅ Verifique se o servidor está rodando (`python run.py`)
- ✅ Verifique se está na mesma rede WiFi

### Problema: CORS error no navegador
- ✅ Verifique se o IP está na lista de origins do CORS
- ✅ Ou use `"origins": "*"` temporariamente para testar (não recomendado em produção)

### Problema: "Network error" no celular
- ✅ Verifique se o celular está na mesma rede WiFi
- ✅ Tente desabilitar temporariamente o firewall para testar
- ✅ Verifique se não há proxy/VPN ativo

---

## 🎯 Resumo Rápido

1. **Frontend:** Use `http://192.168.18.38:5001/api` ao invés de `localhost`
2. **Firewall:** Libere a porta 5001 (passo 2 acima)
3. **Teste:** Acesse `http://192.168.18.38:5001/` no celular
4. **Pronto!** 🎉

