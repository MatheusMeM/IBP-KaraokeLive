# ⚡ Checklist Rápido - Instalação e Testes

## 🚀 Instalação (2 minutos)

### 1. Fazer Backup
```bash
cd /caminho/para/IBP-KaraokeLive
cp modules/screens/score_entry_screen.py modules/screens/score_entry_screen.py.backup
```
✅ Backup criado

---

### 2. Instalar Nova Versão
```bash
cp score_entry_screen_ibp.py modules/screens/score_entry_screen.py
```
✅ Arquivo instalado

---

### 3. Verificar Assets
```bash
# Verificar se existe:
ls assets/images/background_graphic.png
```
- ✅ Arquivo existe → Tudo OK
- ❌ Arquivo não existe → Tela ficará com fundo branco simples (funciona, mas sem gráfico)

---

### 4. Testar
```bash
# Opção A: Teste isolado
python test_score_entry_ibp.py

# Opção B: Aplicação completa
python main.py
```
✅ Aplicação iniciou sem erros

---

## ✅ Checklist de Verificação Visual

### Cores da Marca IBP
- [ ] Fundo branco (não azul escuro)
- [ ] Gráfico de fundo visível (opacidade baixa)
- [ ] Container cinza claro no meio
- [ ] Título "SUA PONTUAÇÃO" em verde
- [ ] Número da pontuação em azul
- [ ] Botão "ENVIAR PONTUAÇÃO" em verde
- [ ] Teclado com fundo cinza escuro
- [ ] Campo de entrada branco com borda azul

### Textos em Português
- [ ] "SUA PONTUAÇÃO" (não "YOUR SCORE")
- [ ] "Digite seu nome:" (não "Enter Your Name")
- [ ] "ENVIAR PONTUAÇÃO" (não "SUBMIT SCORE")
- [ ] Teclas do teclado:
  - [ ] "←" para apagar (não "⌫")
  - [ ] "ESPAÇO" (não "SPACE")
  - [ ] "✓" para OK

### Sem Emojis
- [ ] Avaliação mostra texto, não estrelas
- [ ] Exemplos de avaliação:
  - 90+ pontos: "EXCELENTE!"
  - 75-89 pontos: "MUITO BOM!"
  - 60-74 pontos: "BOM"
  - 40-59 pontos: "REGULAR"
  - 0-39 pontos: "CONTINUE PRATICANDO"

### Estilo dos Botões
- [ ] Botão principal tem bordas arredondadas
- [ ] Botão principal é verde
- [ ] Botão principal fica verde escuro ao clicar
- [ ] Teclas do teclado têm bordas arredondadas
- [ ] Tecla "←" (apagar) é vermelha
- [ ] Tecla "✓" (OK) é verde

---

## ✅ Checklist de Funcionalidade

### Digitação
- [ ] Posso clicar nas teclas e ver as letras
- [ ] Texto aparece no campo branco
- [ ] Limite de 20 caracteres funciona
- [ ] Botão "←" remove último caractere
- [ ] Botão "ESPAÇO" adiciona espaço

### Validação
- [ ] Não posso enviar com campo vazio
- [ ] Não posso enviar com menos de 3 caracteres
- [ ] Mensagens de erro aparecem em vermelho

### Envio
- [ ] Botão "ENVIAR PONTUAÇÃO" funciona
- [ ] Botão "✓" (OK no teclado) também funciona
- [ ] Após enviar, vai para tela de ranking
- [ ] Nome e pontuação aparecem no ranking

---

## 🎨 Comparação Visual Rápida

### ✅ Deve Parecer Assim (CORRETO)
```
┌─────────────────────────────────────┐
│ 🟦 Fundo BRANCO + gráfico           │ ← Branco!
│                                     │
│ ╔═══════════════════════════════╗   │
│ ║ 🟫 Container CINZA CLARO      ║   │ ← Cinza claro
│ ║                               ║   │
│ ║ 🟢 SUA PONTUAÇÃO              ║   │ ← Verde
│ ║ 🔵 78                          ║   │ ← Azul
│ ║ 🔵 MUITO BOM!                  ║   │ ← Texto (não emojis!)
│ ║                               ║   │
│ ║ Digite seu nome:              ║   │ ← Português
│ ║ [campo branco]                ║   │
│ ║                               ║   │
│ ║ 🟢 [ENVIAR PONTUAÇÃO]         ║   │ ← Verde, português
│ ╚═══════════════════════════════╝   │
├─────────────────────────────────────┤
│ ⬛ Teclado CINZA ESCURO             │ ← Cinza escuro
│ [1][2]...[←]  [Q][W]...  [ESPAÇO]  │ ← Português
└─────────────────────────────────────┘
```

### ❌ NÃO Deve Parecer Assim (ERRADO)
```
┌─────────────────────────────────────┐
│ ⬛ Fundo AZUL ESCURO                │ ← ERRADO! Deve ser branco
│                                     │
│ 🟡 YOUR SCORE: 78                   │ ← ERRADO! Deve ser "SUA PONTUAÇÃO"
│ ⭐⭐⭐⭐☆                             │ ← ERRADO! Deve ser texto
│                                     │
│ Enter Your Name:                    │ ← ERRADO! Deve ser português
│ [campo]                             │
│                                     │
│ [SUBMIT SCORE]                      │ ← ERRADO! Deve ser "ENVIAR PONTUAÇÃO"
├─────────────────────────────────────┤
│ [1][2]...[⌫]  [SPACE]              │ ← ERRADO! Deve ser "←" e "ESPAÇO"
└─────────────────────────────────────┘
```

---

## 🔧 Problemas Comuns

### Problema: Fundo está azul escuro, não branco
**Causa:** Arquivo antigo ainda está sendo usado  
**Solução:**
```bash
# Verificar qual arquivo está sendo usado
ls -la modules/screens/score_entry_screen.py

# Reinstalar
cp score_entry_screen_ibp.py modules/screens/score_entry_screen.py

# Reiniciar aplicação
python main.py
```

### Problema: Textos em inglês
**Causa:** Arquivo antigo ainda está sendo usado  
**Solução:** Mesma do problema anterior (reinstalar)

### Problema: Estrelas (emojis) aparecem
**Causa:** Arquivo antigo ainda está sendo usado  
**Solução:** Mesma do problema anterior (reinstalar)

### Problema: Avaliação não aparece
**Causa:** Pontuação não foi definida  
**Solução:**
```python
# No código que chama a tela:
score_screen.set_score(78)  # Definir antes de exibir
```

### Problema: Gráfico de fundo não aparece
**Causa:** Arquivo `background_graphic.png` não existe  
**Solução:**
```bash
# Verificar se existe
ls assets/images/background_graphic.png

# Se não existir, copiar de outra parte do projeto
# Ou a tela funcionará normalmente, só sem o gráfico
```

### Problema: Erro de import
```
ModuleNotFoundError: No module named 'data.ranking_manager'
```
**Solução:**
```bash
# Verificar se o arquivo existe
ls data/ranking_manager.py

# Se não existir, criar um mock:
mkdir -p data
echo "class RankingManager:
    def add_score(self, name, score):
        return True" > data/ranking_manager.py
```

---

## 📊 Status Final

Após completar todos os itens:

```
✅ Instalação
✅ Verificação Visual
✅ Verificação de Funcionalidade
✅ Testes

STATUS: PRONTO PARA PRODUÇÃO! 🎉
```

---

## 💡 Dica Final

**Teste com diferentes pontuações** para ver as avaliações:
```python
score_screen.set_score(95)  # → "EXCELENTE!"
score_screen.set_score(80)  # → "MUITO BOM!"
score_screen.set_score(65)  # → "BOM"
score_screen.set_score(50)  # → "REGULAR"
score_screen.set_score(30)  # → "CONTINUE PRATICANDO"
```

---

## 📞 Próximos Passos

1. ✅ Instalação completa
2. ✅ Testes visuais OK
3. ✅ Testes funcionais OK
4. → Integrar com resto da aplicação
5. → Testar fluxo completo (música → pontuação → ranking)
6. → Deploy em kiosque

---

**Tempo Total de Instalação: ~2 minutos**  
**Tempo de Testes: ~5 minutos**  
**Total: ~7 minutos para ter tudo funcionando! ⚡**

---

*Identidade Visual IBP Aplicada ✅*  
*100% em Português ✅*  
*Sem Emojis ✅*  
*Pronto para Kiosque! 🎤*
