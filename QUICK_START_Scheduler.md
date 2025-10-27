# ⚡ Quick Start: Task Scheduler em 5 Passos

## 🎯 Setup Rápido (5 minutos)

### PASSO 1: Copiar .bat
```
start-ibp-simple.bat → C:\Users\MNDS\Documents\GitHub\IBP-KaraokeLive\
```
✅ Testar: Duplo-clique no .bat (app deve abrir)

---

### PASSO 2: Abrir Task Scheduler
```
Win + R → taskschd.msc → Enter
```

---

### PASSO 3: Criar Tarefa
```
Clicar: "Criar Tarefa..." (não "Básica")
```

**ABA GERAL:**
```
Nome: IBP-KaraokeLive Auto-Start
☑ Executar com privilégios mais altos
```

**ABA GATILHOS → Novo:**
```
Iniciar: Na inicialização
Atrasar: 30 segundos
```

**ABA AÇÕES → Novo:**
```
Programa: C:\Users\MNDS\Documents\GitHub\IBP-KaraokeLive\start-ibp-simple.bat
```

**ABA CONDIÇÕES:**
```
☐ Iniciar apenas se conectado à CA (DESMARCAR)
☐ Parar se alternar para bateria (DESMARCAR)
```

**ABA CONFIGURAÇÕES:**
```
☑ Reiniciar a cada: 1 minuto (3 vezes)
```

---

### PASSO 4: Salvar
```
OK → Digitar senha de admin (se pedir)
```

---

### PASSO 5: Testar
```
Opção A: Botão direito na tarefa → "Executar"
Opção B: Reiniciar computador
```

---

## ✅ Pronto!

App agora abre automaticamente quando ligar o PC.

---

## 🔧 Controles Rápidos

| Ação | Como Fazer |
|------|------------|
| **Executar agora** | Botão direito → Executar |
| **Desabilitar** | Botão direito → Desabilitar |
| **Habilitar** | Botão direito → Habilitar |
| **Remover** | Botão direito → Excluir |

---

## ⚠️ Se Não Funcionar

1. **App não abre no boot:**
   - Aumentar delay para 60 segundos
   - Verificar se tarefa está "Habilitada"

2. **Abre e fecha:**
   - Testar .bat manualmente
   - Verificar caminho do projeto

3. **"Acesso negado":**
   - Marcar "privilégios mais altos"

---

## 📍 Localização

**Task Scheduler:**
```
Iniciar → "Agendador de Tarefas"
```

**Tarefa criada:**
```
Task Scheduler Library
└── IBP-KaraokeLive Auto-Start
```

---

## 💡 Dica Pro

Para ver se funcionou:
```
1. Reiniciar PC
2. Contar: 1... 2... 3... até 40
3. App deve aparecer ✅
```

---

**Guia completo:** GUIA_SIMPLES_TASK_SCHEDULER.md  
**Troubleshooting:** Ver seção "Problemas Comuns" no guia completo
