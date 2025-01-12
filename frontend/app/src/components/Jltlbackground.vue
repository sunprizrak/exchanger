<template>
    <main>
        <div ref="container"> </div>
    </main>
</template>

<script>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';


export default {
    setup() {
        const container = ref(null);

        onMounted(() => {
            const scene = new THREE.Scene();

            // Загрузка HDRI (только для освещения)
            const rgbeLoader = new RGBELoader();
            rgbeLoader.load(
                '/hdri/brown_photostudio_02_4k.hdr',
                (texture) => {
                    texture.mapping = THREE.EquirectangularReflectionMapping;
                    scene.environment = texture;
                },
                undefined, // onProgress
                (error) => {
                    console.error('Ошибка загрузки HDRI:', error);
                }
            );

            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 10;

            const renderer = new THREE.WebGLRenderer({antialias: true});
            renderer.setSize(window.innerWidth, window.innerHeight);
            container.value.appendChild(renderer.domElement);

            // Подключение управления
            console.warn('DeviceOrientation API недоступен. Включаем альтернативное управление.');
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true; // Включаем плавность
            controls.dampingFactor = 0.25; // Мощность плавности
            controls.screenSpacePanning = false; // Запрещаем панорамирование по экрану
            controls.enableZoom = false

            // Загружаем модель GLTF
            const loader = new GLTFLoader();

            loader.load(
                '/bitcoin/scene.gltf', // путь к модели
                (gltf) => {
                    const coin = gltf.scene; // Получаем объект сцены из загруженной модели

                    // Создаём группу
                    const coinGroup = new THREE.Group();
                    scene.add(coinGroup);
                    coinGroup.add(coin);

                    coin.scale.set(0.01, 0.01, 0.01); // Устанавливаем масштаб

                    // Центрируем модель
                    const box = new THREE.Box3().setFromObject(coin); // Получаем границы модели
                    const center = box.getCenter(new THREE.Vector3()); // Получаем центр модели
                    coin.position.sub(center); // Смещаем позицию модели, чтобы центр был в (0, 0, 0)

                    const size = box.getSize(new THREE.Vector3()); // Размеры модели

                    // Поднимаем группу вверх, не изменяя центр модели
                    coinGroup.position.y += size.y / 1.5; // Поднимаем точку вращения не влияя на вращение модели





                    // Анимация
                    const animate = function () {
                        requestAnimationFrame(animate);

                        // Анимация модели (если нужна)
                        // Если у модели есть анимация, можно добавить сюда код для её воспроизведения.

                        renderer.render(scene, camera);
                    };

                    animate();
                },
                // Прогресс загрузки
                (xhr) => {
                  console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
                },
                // Обработка ошибок
                (error) => {
                  console.error('Error loading the model', error);
                }
            );

            // Адаптация под изменение размера окна
            window.addEventListener('resize', () => {
                renderer.setSize(window.innerWidth, window.innerHeight);
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
            });
        });

        return { container };
    },
};
</script>

<style>
main {
    height: calc(100vh - 60px);
    width: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}
main div {
    width: 100%;
    height: 100%;
}
main div canvas {
    width: 100%;
    height: 100%;
}

</style>
