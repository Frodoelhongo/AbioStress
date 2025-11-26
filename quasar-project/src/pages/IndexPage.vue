<template>
  <q-tab-panels v-model="selectedTab" animated swipeable class="main-panels">
    <q-tab-panel name="home" class="q-pa-none">
      <section id="home" class="home-section">
        <!-- Cuadro de título superior izquierdo -->
        <div class="top-title-box">
          <h1 class="top-title-text">
            AbioStress-TWAS: Cultivos Más Fuertes con Inteligencia Artificial
          </h1>
        </div>

        <!-- Carrusel automático de información -->
        <div class="carousel-section">
          <q-carousel
            v-model="currentSlide"
            transition-prev="slide-right"
            transition-next="slide-left"
            animated
            swipeable
            control-color="grey-8"
            arrows
            class="carousel-container"
            height="600px"
            :autoplay="15000"
          >
            <!-- Slide 1: Bienvenida -->
            <q-carousel-slide name="1" class="q-pa-none">
              <div class="slide-background">
                <div class="info-card-compact info-card-welcome">
                  <h3 class="welcome-title">¿Para qué sirve este servidor web?</h3>
                  <p class="welcome-text">
                    Ayuda a seleccionar las variedades de cultivo más adecuadas según las características de su suelo, mejorando su producción y contribuyendo a la seguridad alimentaria de su comunidad.
                  </p>
                </div>
              </div>
            </q-carousel-slide>

            <!-- Slide 2: Resiliencia -->
            <q-carousel-slide name="2" class="q-pa-none">
              <div class="slide-background">
                <div class="info-card-compact">
                  <h3 class="card-subtitle">
                    Nuestro sistema identifica las líneas de cultivo con mejores mecanismos de resiliencia frente a:
                  </h3>
                  <div class="row q-mt-md items-center">
                    <div class="col-4 flex flex-center">
                      <img src="/images/drougth.jpg" class="drought-image-small" />
                    </div>
                    <div class="col-8 flex column justify-center">
                      <ul class="stress-list-compact">
                        <li><strong>Sequía</strong></li>
                        <li><strong>Salinidad</strong></li>
                        <li><strong>Temperaturas extremas</strong> (calor o frío)</li>
                        <li><strong>Suelos con metales pesados</strong></li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </q-carousel-slide>

            <!-- Slide 3: Cultivos disponibles -->
            <q-carousel-slide name="3" class="q-pa-none">
              <div class="slide-background">
                <div class="slide-title-box">
                  <h3 class="slide-title-text">Cultivos disponibles para consulta</h3>
                </div>
                <div class="info-card-compact">
                  <div class="crops-grid-compact">
                    <div class="crop-item-compact">
                      <div class="crop-circle-compact">
                        <img src="/images/TomateChat.png" class="crop-img-compact" />
                      </div>
                      <p class="crop-label-compact">Tomate</p>
                    </div>
                    <div class="crop-item-compact">
                      <div class="crop-circle-compact">
                        <img src="/images/cotton.jpg" class="crop-img-compact" />
                      </div>
                      <p class="crop-label-compact">Algodón</p>
                    </div>
                    <div class="crop-item-compact">
                      <div class="crop-circle-compact">
                        <img src="/images/maiz.jpg" class="crop-img-compact" />
                      </div>
                      <p class="crop-label-compact">Maíz</p>
                    </div>
                    <div class="crop-item-compact">
                      <div class="crop-circle-compact">
                        <img src="/images/SandiaChat.png" class="crop-img-compact" />
                      </div>
                      <p class="crop-label-compact">Sandía</p>
                    </div>
                    <div class="crop-item-compact">
                      <div class="crop-circle-compact">
                        <img src="/images/Sorghum.jpg" class="crop-img-compact" />
                      </div>
                      <p class="crop-label-compact">Sorgo</p>
                    </div>
                  </div>
                </div>
              </div>
            </q-carousel-slide>
          </q-carousel>
        </div>
      </section>
    </q-tab-panel>

    <q-tab-panel name="database" class="panel-with-background">
      <db-table />
    </q-tab-panel>

    <q-tab-panel name="interpretation" class="panel-with-background">
      <interpretation-panel :result="predictionResult" />
    </q-tab-panel>

    <q-tab-panel name="gene-prediction" class="panel-with-background">
      <section id="gene-prediction">
        <genes-prediction @prediction-updated="predictionResult = $event" />
      </section>
    </q-tab-panel>

    <q-tab-panel name="about-us" class="panel-with-background">
      <about-us />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue';
import DbTable from 'src/components/DbTable.vue';
import AboutUs from 'src/components/AboutUs.vue';
import GenesPrediction from 'src/components/GenesPrediction.vue';
import InterpretationPanel from 'src/components/InterpretationPanel.vue';

const selectedTab = defineModel();
const currentSlide = ref('1');

// Estado compartido para el resultado de la predicción
const predictionResult = ref<{
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score?: number; stresses?: string[] } | string>
} | null>(null);

// Proveer el resultado para que los componentes hijos puedan acceder
provide('predictionResult', predictionResult);
</script>

<style scoped>
/* Fondo para todos los paneles */
.main-panels {
  background-image: url('/images/field-crop.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: calc(100vh - 70px);
}

.panel-with-background {
  background: rgba(184, 201, 217, 0.35);
  min-height: calc(100vh - 70px);
}

/* Sección principal */
.home-section {
  min-height: calc(100vh - 70px);
  background: transparent;
  position: relative;
}

/* Cuadro de título superior izquierdo */
.top-title-box {
  position: absolute;
  top: 20px;
  left: 30px;
  background: rgba(255, 255, 255, 0.75);
  border-radius: 20px;
  padding: 15px 28px;
  max-width: 400px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  z-index: 10;
  backdrop-filter: blur(8px);
}

.top-title-text {
  font-size: 22px;
  font-weight: 700;
  color: #000;
  margin: 0;
  line-height: 1.3;
}

/* Sección del carrusel */
.carousel-section {
  padding: 0;
  background: transparent;
  min-height: calc(100vh - 200px);
  padding-top: 150px;
}

.carousel-container {
  background: transparent;
}

.slide-background {
  width: 100%;
  height: 100%;
  background-image: url('/images/field-crop.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px 80px;
}

/* Caja de información blanca compacta */
.info-card-compact {
  background: rgba(255, 255, 255, 0.85);
  border-radius: 35px;
  padding: 25px 35px;
  max-width: 750px;
  width: auto;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.25);
}

.card-subtitle {
  font-size: 24px;
  font-weight: 600;
  color: #000;
  text-align: center;
  margin: 0 0 15px 0;
  line-height: 1.4;
}

/* Imagen de sequía pequeña */
.drought-image-small {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* Lista de estrés compacta */
.stress-list-compact {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 20px;
  line-height: 1.6;
}

.stress-list-compact li {
  margin-bottom: 12px;
  color: #000;
}

.stress-list-compact li::before {
  content: '• ';
  color: #3d4f1f;
  font-weight: bold;
  font-size: 28px;
  margin-right: 12px;
}

.stress-bold {
  font-weight: 700;
}

/* Título del slide separado */
.slide-title-box {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.85);
  border-radius: 30px;
  padding: 15px 40px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.slide-title-text {
  font-size: 26px;
  font-weight: 600;
  color: #000;
  margin: 0;
  text-align: center;
}

/* Grid de cultivos compacto */
.crops-grid-compact {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  padding: 20px 10px;
  flex-wrap: wrap;
}

.crop-item-compact {
  text-align: center;
}

.crop-circle-compact {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  background: white;
}

.crop-img-compact {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.crop-label-compact {
  font-size: 18px;
  font-weight: 600;
  color: #000;
  margin: 0;
}

/* Slide 0: Bienvenida */
.info-card-welcome {
  max-width: 650px;
  text-align: center;
}

.welcome-title {
  font-size: 28px;
  font-weight: 700;
  color: #000;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

.welcome-text {
  font-size: 20px;
  font-weight: 400;
  color: #000;
  margin: 0;
  line-height: 1.6;
}

/* Slide 3: Solo imagen */
.slide-fullimage {
  padding: 0;
  background: none;
}

.full-field-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
