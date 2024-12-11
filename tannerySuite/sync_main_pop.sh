#!/bin/bash

# Passo 1: Passa al ramo pop
git checkout pop

# Passo 2: Aggiorna il ramo pop con le modifiche remote
git pull origin pop

# Passo 3: Passa al ramo main
git checkout main

# Passo 4: Aggiorna il ramo main con le modifiche remote
git pull origin main

# Passo 5: Torna al ramo pop
git checkout pop

# Passo 6: Unisci le modifiche da main a pop
git merge main

# Passo 7: Se la merge è riuscita senza conflitti, esegui il push delle modifiche
if [ $? -eq 0 ]; then
    git push origin pop
    echo "Merge riuscito e push completato!"
else
    echo "Merge fallito a causa di conflitti. Risolvi i conflitti manualmente."
fi

