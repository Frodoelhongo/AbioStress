<template>
  <section id="about-us" class="content-section">
    <div class="about-container">
      <!-- Texto principal -->
      <div class="about-box">
        <p class="about-text">
          Somos estudiantes de la Licenciatura en Ingeniería Bioquímica en la Facultad de Ciencias
          Biológicas de la Universidad Autónoma de Coahuila. Actualmente formamos parte del
          Laboratorio de Biorremediación, dirigido por el Dr. Nagamani Balagurusamy.
        </p>
      </div>

      <!-- Perfiles de autoras -->
      <div class="profiles-container">
        <!-- Angela -->
        <div class="profile-row">
          <div class="profile-image">
            <img src="/images/Angela.png" alt="Angela Martínez" />
          </div>
          <div class="profile-info">
            <h3 class="profile-name">Angela Martínez</h3>
            <p class="profile-description">
              Estudiante de 7mo semestre de la carrera de ingeniería bioquímica con interés en las áreas de biología molecular, biotecnología y bioinformática.
            </p>
            <p class="profile-email">angela.medina@uadec.edu.mx</p>
          </div>
        </div>

        <!-- Frida -->
        <div class="profile-row">
          <div class="profile-image">
            <img src="/images/Frida.png" alt="Frida Orozco" />
          </div>
          <div class="profile-info">
            <h3 class="profile-name">Frida Orozco</h3>
            <p class="profile-description">
              Estudiante de 7mo semestre de la carrera de ingeniería bioquímica, interesada en las áreas de bioinformática, biología molecular y bioprocesos.
            </p>
            <p class="profile-email">fridaorozco@uadec.edu.mx</p>
          </div>
        </div>

        <!-- Lily -->
        <div class="profile-row">
          <div class="profile-image">
            <img src="/images/Lily.png" alt="Liliana Torres" />
          </div>
          <div class="profile-info">
            <h3 class="profile-name">Liliana Torres</h3>
            <p class="profile-description">
              Estudiante de 7mo semestre de la carrera de ingeniería bioquímica con interés en áreas de biología molecular, biotecnología y bioinformática.
            </p>
            <p class="profile-email">torresliliana@uadec.edu.mx</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script setup lang="ts">
</script>

<style scoped lang="sass">
.content-section
  display: flex
  align-items: flex-start
  justify-content: center
  min-height: calc(100vh - 100px)
  padding: 40px 20px

.about-container
  max-width: 900px
  width: 100%

.about-box
  background: rgba(255, 255, 255, 0.98)
  border-radius: 16px
  padding: 25px 40px
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)
  backdrop-filter: blur(8px)
  margin-bottom: 40px
  max-width: 850px
  margin-left: auto
  margin-right: auto

.about-text
  font-size: 17px
  font-weight: 400
  color: #333
  margin: 0
  line-height: 1.6
  text-align: center

.profiles-container
  display: flex
  flex-direction: column
  gap: 30px

.profile-row
  position: relative
  display: flex
  align-items: center
  gap: 20px
  margin-bottom: 20px

  &:nth-child(even)
    flex-direction: row-reverse

.profile-image
  flex-shrink: 0
  width: 140px
  height: 140px
  border-radius: 50%
  overflow: hidden
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3)
  border: 4px solid rgba(255, 255, 255, 0.9)
  z-index: 2

  img
    width: 100%
    height: 100%
    object-fit: cover

.profile-info
  flex: 1
  background: rgba(245, 245, 240, 0.95)
  border-radius: 20px
  padding: 20px 30px 20px 40px
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)
  backdrop-filter: blur(8px)
  margin-left: -25px
  z-index: 1
  display: flex
  flex-direction: column
  gap: 8px
  max-width: 650px

  .profile-row:nth-child(even) &
    margin-left: 0
    margin-right: -25px
    padding: 20px 40px 20px 30px

.profile-name
  font-size: 22px
  font-weight: 700
  color: #2c3e50
  margin: 0
  letter-spacing: 0.5px

.profile-description
  font-size: 17px
  font-weight: 400
  color: #444
  margin: 0
  line-height: 1.6
  text-align: justify

.profile-email
  font-size: 13px
  font-weight: 500
  color: #555
  margin: 0
  margin-top: 5px
</style>
