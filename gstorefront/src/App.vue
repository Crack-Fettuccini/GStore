<template>
    <router-view/>
    <div class="blur"></div>
</template>

<style>
#app {
  font-family: -apple-system, system-ui, BlinkMacSystemFont, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  transition: opacity 0.3s linear;
}
body *{
  margin-right:0% !important;
}
a {
  text-decoration: none !important;  
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

div #authentication{
  align-items: end;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s linear;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
  #title_card {
    position: static;
    text-align: center;
    margin-top:3% !important;
    font-weight:200;
  }

  #shows {
    margin-top: 50px !important; 
  }
  .c-container{
    position: relative;
    border-radius: 5%;
    perspective: 1000px;
    width: 16.2rem  !important;
    height: 21.6rem !important;
    margin: 1rem !important;
    margin-top: .9 !important;
    margin-left: 1.2 !important;
    margin-bottom: .9 !important;
    margin-right: 1.2 !important;
    display: inline-block;
    opacity: 0;
    transform: translateY(20px);
    animation: fade-in .5s ease-in-out forwards;
  }
  .flex-container{
    opacity: 0;
    transform: translateY(20px);
    animation: fade-in .5s ease-in-out forwards;
  }
  
  .navbar{
    z-index: 1;
    position: -webkit-sticky !important; /* Safari */
    position: sticky !important;
    top: 0;
    padding-top: 14px !important;
    padding-bottom: 14px !important;
    background-color: #ffffffaa;
    opacity: 0;
    animation: swap .5s ease-in-out forwards;
  }

  body{
    background:#ffffff77 url('~@/assets/output.jpg') !important;
    background-position: bottom;
    background-repeat: no-repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
  }

  .blur{
    position: fixed !important;
    bottom:0;
    z-index: -100;
    width:100% !important;
    height: 100vh !important;
    -webkit-backdrop-filter: blur(5px) !important;
    backdrop-filter: blur(5px) !important;

  }
  .new-container {
    position: relative;
    border-radius: 20%;
    perspective: 1000px;
    width: 18rem;
    min-height: 20rem;
    display: inline-block;
    opacity: 0;
    transform: translateY(20px);
    animation: fade-in .5s ease-in-out forwards;
    cursor: pointer;
  }
  .card {
    border-radius: 5% !important;
    position: relative;
    width: 100%  !important;
    height: 100%  !important;
    transform-style: preserve-3d;
    transition: transform 0.8s;
  }


  .front,
  .back {
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    overflow:hidden;
    border-radius: 5%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .front {
    transform: rotateY(0deg);
  }

  .back {
    position: absolute;
    transform: rotateY(180deg) translateZ(1px);
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
  }


  .new-front,
  .new-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    overflow:hidden;
  }

  .new-front {
    border-radius: 20%;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transform: rotateY(0deg);
  }

  .new-back {
    border-radius: 20%;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transform: rotateY(180deg) translateZ(1px);
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
  }

  .c-container:hover .card:not(.outofstock) {
    transform: rotateY(180deg);
  }
  .new-container:not(.new-show-visible):hover .card {
    transform: scale(1.05);
  }

  @keyframes fade-in {
    0% {
      opacity: 0;
      transform: translateY(50px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  @keyframes swap {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  @keyframes expandAnimation {
    from {
      height: 20rem;
      border-radius:20%
    }
    to {
      height: 40rem;
      border-radius:10%
    }
  }

  .new-show-form {
  animation-name: expandAnimation;
  animation-duration: 0.8s;
  animation-timing-function: ease;
  animation-fill-mode: forwards;
  }

  .overlay {
      position: fixed;
      top: 70px;
      left: 0;
      right: 0;
      bottom: 0;

  animation: overlayer 1s ease-in-out forwards;
  }
  @keyframes overlayer {
    from {
      backdrop-filter: blur(0);
      -webkit-backdrop-filter: blur(0);

    }
    to {
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
    }
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s linear;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  .accordion-button{
    color:white !important;
    font-weight: 600 !important;
  }
  .accordion-body{
    text-align:left !important;
  }

  .accordion-item.Pending .accordion-button{
    background-color:#ffc107 !important;
  }
  .accordion-item.Pending{
    border-color:#ffc107 !important;
  }

  .accordion-item.Approved .accordion-button{
    background-color:#198754 !important;
  }
  .accordion-item.Approved{
    border-color:#198754 !important;
  }

  .accordion-item.Rejected .accordion-button{
    background-color:#dc3545 !important;
  }
  .accordion-item.Rejected{
    border-color:#dc3545 !important;
  }

  .accordion-item.Pending .accordion-collapse{
    background-color:#ffc10777 !important;
  }

  .accordion-item.Approved .accordion-collapse{
    background-color:#19875477 !important;
  }

  .accordion-item.Rejected .accordion-collapse{
    background-color:#dc354577 !important;
  }

  button{
    cursor: pointer !important;
  }
</style>
