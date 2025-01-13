<template>
    <div class="button-group">
        <div
            v-for="(button, index) in buttons"
            :key="index"
            :class="{ active: button.isActive }"
            @click="toggleActive(index)"
        >
            <svg v-if="index === 0" viewBox="0 0 512 512">
                <path d="M287.03 20c-39.133.48-79.73 15.297-117 45.938h80.47v43.188c52.76-29.75 114.592-31.588 163.938.03l-18.188 9.72 64.688 50.72-3.75-83.314-26.407 14.126C395.99 48.792 345.038 20.644 290.907 20c-1.288-.015-2.583-.016-3.875 0zm-268 64.625v212.75h212.782V84.625H19.032zm50.282 26.03H205.78v138.939h-18.718v-120.25H69.313v-18.688zm3.344 38.126l90.094 91.845-13.344 13.094-90.094-91.845 13.344-13.094zm206.656 61.75v212.782h212.75v-212.78h-212.75zm50.25 26.064h136.469V375.5h-18.686V255.28h-117.78l-.002-18.686zm3.344 38.094l90.125 91.875-13.342 13.062-90.125-91.844 13.343-13.092zm-278.53 63.656l3.75 83.312 23.312-12.47c60.927 88.637 169.99 106.485 259.625 32.814h-80.439v-43.188c-52.08 29.38-113 31.544-162.03 1.188l20.436-10.938-64.655-50.718z"/>
            </svg>
            <svg v-if="index === 1" viewBox="0 0 32 32">
                <path d="M0 26.016v-20q0-2.496 1.76-4.256t4.256-1.76h20q2.464 0 4.224 1.76t1.76 4.256v20q0 2.496-1.76 4.224t-4.224 1.76h-20q-2.496 0-4.256-1.76t-1.76-4.224zM4 26.016q0 0.832 0.576 1.408t1.44 0.576h20q0.8 0 1.408-0.576t0.576-1.408v-20q0-0.832-0.576-1.408t-1.408-0.608h-20q-0.832 0-1.44 0.608t-0.576 1.408v20zM8 24v-4h4v4h-4zM8 18.016v-4h4v4h-4zM8 12v-4h4v4h-4zM14.016 24v-4h9.984v4h-9.984zM14.016 18.016v-4h9.984v4h-9.984zM14.016 12v-4h9.984v4h-9.984z"></path>
            </svg>
        </div>

        <svg class="svg-filters">
            <defs>
                <radialGradient id="active" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#ebf7ff;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#b3e1ff;stop-opacity:1" />
                </radialGradient>

                <filter id="inset-shadow">
                    <feOffset
                        dx='-1'
                        dy='1'
                    />
                    <feGaussianBlur
                        stdDeviation='.7'
                        result='offset-blur'
                    />
                    <feComposite
                        operator='out'
                        in='SourceGraphic'
                        in2='offset-blur'
                        result='inverse'
                    />
                    <feFlood
                        flood-color='black'
                        flood-opacity='0.05'
                        result='color'
                    />
                    <feComposite
                        operator='in'
                        in='color'
                        in2='inverse'
                        result='shadow'
                    />
                    <feComposite
                        operator='over'
                        in='shadow'
                        in2='SourceGraphic'
                    />
                </filter>
            </defs>
        </svg>
    </div>
</template>


<script>
export default {
    data() {
        return {
            buttons: [
                {
                    isActive: true,
                    route: '/',
                },
                {
                    isActive: false,
                    route: '/orders',
                }
            ]
        };
    },
    methods: {
        toggleActive(index) {
             // Деактивируем все кнопки
            this.buttons.forEach((button, i) => {
                button.isActive = i === index;
            });

            // Перенаправление на маршрут
            this.$router.push(this.buttons[index].route);
        }
    }
};
</script>



<style scoped>
.button-group {
    position: relative;
    z-index: 2;
    display: flex;
    height: 50px;
    background-color: #000;
    border-radius: 7px;
    padding: 4px;
}

.button-group > div {
    cursor: pointer;
    flex: 1;
    width: 80px;
    background-image: linear-gradient(to top, #242424 0%, #303030 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 1px;
    transition: 0.2s;
    font-size: 1.5em;
    box-shadow: inset 0 20px 4px -21px rgba(255,255,255,0.4), 0 19px 13px 0 rgba(0,0,0,0.3);
    color: #181818;
    position: relative;
    z-index: 2;
}

.button-group > div:before {
    content: "";
    display: block;
    width: 0.8em;
    height: 50px;
    transition: 0.1s;
    background-image: radial-gradient(circle 30px at center, #ebf7ff 0%, #b3e1ff 47%, #b3e1ff 100%);
    position: absolute;
    filter: blur(15px);
    top: 50%;
    left: 50%;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    opacity: 0;
}

.button-group > div:after {
    content: "";
    display: block;
    height: 70px;
    width: 1px;
    position: absolute;
    border-radius: 50%;
    z-index: -1;
    opacity: 0;
    transition: 0.2s;
    filter: blur(0px);
    box-shadow: -75px 0 0px 0px rgba(179,225,255,0.3), 74px 0 0px 0px rgba(179,225,255,0.35);
}

.button-group > div svg {
    width: 24px;
    height: 24px;
    position: relative;
    display: block;
    fill: #181818;
    filter: drop-shadow(0 1px 1px rgba(255,255,255,0.15)) url("#inset-shadow");
}

.button-group > div.active {
    background-image: linear-gradient(to top, #151515 0%, #1d1d1d 100%);
    box-shadow: inset 0 16px 14px -21px transparent, 0 0px 13px 0 rgba(0,0,0,0.3), inset 0 0 7px 2px rgba(0,0,0,0.4);
    z-index: 0;
}

.button-group > div.active:before {
    width: 1em;
    height: 1em;
    opacity: 0.8;
}

.button-group > div.active:after {
    opacity: 0;
}

.button-group > div.active svg {
    fill: url("#active");
    filter: drop-shadow(0 1px 1px rgba(255,255,255,0));
}

.button-group div:first-of-type {
    border-radius: 4px 0 0 4px;
}

.button-group div:first-of-type:after {
    box-shadow: -85px 0 18px 1px transparent, 83px 0 12px 1px #b3e1ff;
}

.button-group div:last-of-type {
    border-radius: 0 4px 4px 0;
}

.button-group div:last-of-type:after {
    box-shadow: -85px 0 18px 1px #b3e1ff, 83px 0 12px 1px transparent;
}

.svg-filters {
    height: 0;
    width: 0;
}
</style>