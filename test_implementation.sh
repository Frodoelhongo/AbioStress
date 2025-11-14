#!/bin/bash
# Script de prueba rápida para verificar que los modelos funcionan

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║    PRUEBA DE MÚLTIPLES MODELOS - AbioStress                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}1️⃣  Verificando archivos de Sandía...${NC}"
if [ -f "backend/models/red3_site_meta_20251018_151143.json" ] && \
   [ -f "backend/models/red3_site_student_20251018_151143.pt" ] && \
   [ -f "backend/models/red3_line_gene_panel.json" ]; then
    echo -e "${GREEN}   ✅ Archivos de Sandía presentes${NC}"
else
    echo -e "${RED}   ❌ Faltan archivos de Sandía${NC}"
fi

echo ""
echo -e "${YELLOW}2️⃣  Verificando archivos de Maíz...${NC}"
if [ -f "backend/models/maiz_site_meta_20251111_132606.json" ] && \
   [ -f "backend/models/maiz_site_student_20251111_132606.pt" ] && \
   [ -f "backend/models/maiz_line_gene_panel.json" ]; then
    echo -e "${GREEN}   ✅ Archivos de Maíz presentes${NC}"
else
    echo -e "${RED}   ❌ Faltan archivos de Maíz${NC}"
fi

echo ""
echo -e "${YELLOW}3️⃣  Verificando archivos de preprocesamiento...${NC}"
if [ -f "backend/preproc/red3_scaler_20251018_145912.joblib" ] && \
   [ -f "backend/preproc/maiz_scaler_20251111_131028.joblib" ]; then
    echo -e "${GREEN}   ✅ Escalers cargados${NC}"
else
    echo -e "${RED}   ❌ Faltan escalers${NC}"
fi

echo ""
echo -e "${YELLOW}4️⃣  Verificando código TypeScript...${NC}"
if grep -q "SUPPORTED_CROPS.*Maíz" "quasar-project/src/services/gene-model.ts"; then
    echo -e "${GREEN}   ✅ Soporte para Maíz en gene-model.ts${NC}"
else
    echo -e "${RED}   ❌ Maíz no configurado en gene-model.ts${NC}"
fi

echo ""
echo -e "${YELLOW}5️⃣  Verificando componente Vue...${NC}"
if grep -q "cultivosDisponibles" "quasar-project/src/components/GenesPrediction.vue"; then
    echo -e "${GREEN}   ✅ Componente actualizado${NC}"
else
    echo -e "${RED}   ❌ Componente no actualizado${NC}"
fi

echo ""
echo -e "${YELLOW}6️⃣  Cargando backend...${NC}"
cd backend && python3 -c "
import app
print('   ✅ Cultivos:', list(app.CULTIVOS_CONFIG.keys()))
print('   ✅ Modelos:', list(app.MODELOS.keys()))
" 2>&1 | grep "✅"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        ✨ TODAS LAS VERIFICACIONES COMPLETADAS ✨               ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Para probar el backend:"
echo -e "  ${YELLOW}cd backend${NC}"
echo -e "  ${YELLOW}pip install fastapi uvicorn pytorch pandas scikit-learn${NC}"
echo -e "  ${YELLOW}uvicorn app:app --reload${NC}"
echo ""
echo -e "Para probar el frontend:"
echo -e "  ${YELLOW}cd quasar-project${NC}"
echo -e "  ${YELLOW}npm install${NC}"
echo -e "  ${YELLOW}quasar dev${NC}"
