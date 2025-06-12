import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.01, 10000 );

const SCALE_FACTOR = 0.00000001;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize( window.innerWidth, window.innerHeight );

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
labelRenderer.domElement.style.pointerEvents = 'none';

const controls = new OrbitControls( camera, renderer.domElement );


camera.position.z = 5;

function parseCfgValues(text) {
    const result = {};
    const lines = text.split('\n');
    for (let line of lines) {
        line = line.trim();
        if (line.startsWith('//') || !line.includes('=')) continue;
        const [key, value] = line.split('=').map(s => s.trim());
        if (!(key in result))
        result[key] = value;
    }
    return result;
}

function buildBodyTree(configs) {
    const bodies = {};
    const children = {};

    for (const cfg of configs) {
        const values = parseCfgValues(cfg.content);
        const internalName = values.name;
        const displayName = values.displayName || internalName;
        const referenceBody = values.referenceBody || 'Sun';
        const radius = parseFloat(values.radius || '1000');
        const semiMajorAxis = parseFloat(values.semiMajorAxis || '0');
        const eccentricity = parseFloat(values.eccentricity || '0');
        const inclination = parseFloat(values.inclination || '0');

        bodies[internalName] = {
            name: displayName,
            internalName,
            displayName,
            referenceBody,
            radius,
            semiMajorAxis,
            eccentricity,
            inclination,
            children: []
        };

        if (!children[referenceBody]) children[referenceBody] = [];
        children[referenceBody].push(internalName);
    }

    for (const name in bodies) {
        const b = bodies[name];
        b.children = (children[name] || []).map(childName => bodies[childName]);
    }

    return children['Sun'] ? children['Sun'].map(name => bodies[name]) : [];
}

function createOrbitLine(semiMajorAxis, eccentricity = 0, inclination = 0) {
    const segments = 128;
    const points = [];
    const b = semiMajorAxis * Math.sqrt(1 - eccentricity * eccentricity);
    const rotation = new THREE.Matrix4().makeRotationX(THREE.MathUtils.degToRad(inclination));

    for (let i = 0; i <= segments; i++) {
        const angle = (i / segments) * 2 * Math.PI;
        const x = Math.cos(angle) * semiMajorAxis;
        const z = Math.sin(angle) * b;
        const point = new THREE.Vector3(x, 0, z).applyMatrix4(rotation);
        points.push(point);
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0x888888 });
    return new THREE.LineLoop(geometry, material);
}

document.getElementById('load-button').addEventListener('click', async () => {
    const { planetConfigs, iconPaths } = await loadCfgFilesRecursively();
    console.log('Loaded CFG files:', planetConfigs);
    console.log(`Total configs loaded: ${planetConfigs.length}`);
    document.getElementById('load-button').remove()

    const system = buildBodyTree(planetConfigs);
    console.log('System tree rooted at Sun:', system);
    const bodyMeshes = [];
    let currentFocus = 0;

    const textureBasePathMap = {};
    for (const cfg of planetConfigs) {
        const basePath = cfg.name.split('/').slice(0, -1).join('/');
        const values = parseCfgValues(cfg.content);
        const displayName = values.displayName || values.name;
        textureBasePathMap[displayName] = basePath;
    }

    let displayedBodyCount = 0;

    function addBodiesToScene(bodies, parentPosition = new THREE.Vector3(0, 0, 0), visited = new Set(), textureBasePathMap) {
        const orbitSpacing = 0.05;

        for (const body of bodies) {
            if (visited.has(body.internalName)) {
                console.warn(`Skipping already visited body: ${body.name} (${body.internalName})`);
                continue; // Prevent cycles
            }
            visited.add(body.internalName);
            console.log(`Placing body: ${body.name}, semiMajorAxis: ${body.semiMajorAxis}, radius: ${body.radius}`);

            const angle = Math.random() * Math.PI * 2;
            const distance = body.semiMajorAxis * SCALE_FACTOR + orbitSpacing;
            // Calculate position along the orbit using eccentricity and inclination, matching createOrbitLine
            const b = distance * Math.sqrt(1 - (body.eccentricity || 0) * (body.eccentricity || 0));
            const orbitRotation = new THREE.Matrix4().makeRotationX(THREE.MathUtils.degToRad(body.inclination || 0));
            const orbitAngle = angle;
            const pos = new THREE.Vector3(
                Math.cos(orbitAngle) * distance,
                0,
                Math.sin(orbitAngle) * b
            ).applyMatrix4(orbitRotation);
            const position = parentPosition.clone().add(pos);

            const geometry = new THREE.SphereGeometry(body.radius * SCALE_FACTOR, 16, 16);
            const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.copy(position);
            mesh.userData = { name: body.name };
            scene.add(mesh);

            displayedBodyCount++;

            if (distance > 0) {
                const orbitLine = createOrbitLine(distance, body.eccentricity || 0, body.inclination || 0);
                orbitLine.position.copy(parentPosition);
                scene.add(orbitLine);
            }

            bodyMeshes.push(mesh);

            const labelDiv = document.createElement('div');
            labelDiv.className = 'label';
            labelDiv.textContent = body.name;
            labelDiv.style.marginTop = '-1em';
            labelDiv.style.color = 'white';
            labelDiv.style.fontSize = '12px';
            labelDiv.style.textAlign = 'center';
            labelDiv.style.cursor = 'pointer';
            // Enable click interactions on each label; override inherited pointer-events: none
            labelDiv.style.pointerEvents = 'auto';

            labelDiv.addEventListener('click', () => {
                const target = mesh.position;
                const offset = new THREE.Vector3(0, 0, body.radius * SCALE_FACTOR * 10 + 1);
                camera.position.copy(target.clone().add(offset));
                controls.target.copy(target);
            });

            const label = new CSS2DObject(labelDiv);
            label.position.set(0, body.radius * SCALE_FACTOR * 1.5 + 0.1, 0);
            mesh.add(label);

            // Add icon as CSS2DRenderer icon instead of sprite
            const cfg = planetConfigs.find(cfg => parseCfgValues(cfg.content).name === body.internalName);
            if (!cfg) {
                console.warn(`No matching config found for body: ${body.name} (${body.internalName})`);
            }
            if (cfg) {
                const values = parseCfgValues(cfg.content);
                if (!values) {
                    console.warn(`Failed to parse config for body: ${body.name} (${body.internalName})`);
                }
                if (values && values.iconTexture) {
                    const iconFileName = values.iconTexture.split('/').pop();
                    const iconUrl = iconPaths[iconFileName];
                    if (iconUrl) {
                        const iconDiv = document.createElement('img');
                        iconDiv.src = iconUrl;
                        iconDiv.style.width = '20px';
                        iconDiv.style.height = '20px';
                        iconDiv.style.pointerEvents = 'none';
                        iconDiv.style.marginBottom = '1em';
                        const iconLabel = new CSS2DObject(iconDiv);
                        iconLabel.position.set(0, body.radius * SCALE_FACTOR * 1.5 + 0.25, 0);
                        mesh.add(iconLabel);
                    } else {
                        console.warn(`Icon file not found for body: ${body.name}, icon: ${iconFileName}`);
                    }
                }
            }

            if (body.children.length > 0) {
                console.log(`Adding children of ${body.name}: ${body.children.map(c => c.name).join(', ')}`);
                addBodiesToScene(body.children, position, visited, textureBasePathMap);
            } else {
                console.log(`Body ${body.name} has no children.`);
            }
        }
    }

    addBodiesToScene(system, new THREE.Vector3(0, 0, 0), new Set(), textureBasePathMap);
    console.log(`Displayed total bodies: ${displayedBodyCount}`);

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            if (bodyMeshes.length === 0) return;
            currentFocus = (currentFocus + 1) % bodyMeshes.length;
            const target = bodyMeshes[currentFocus].position;
            const body = bodyMeshes[currentFocus];
            // Use the same offset logic as the label click handler for consistency
            const offset = new THREE.Vector3(0, 0, body.geometry.parameters.radius * SCALE_FACTOR * 10 + 1);
            camera.position.copy(target.clone().add(offset));
            controls.target.copy(target);
        }
    });
    document.body.appendChild( renderer.domElement );
    document.body.appendChild(labelRenderer.domElement);


    animate();
})

function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
    labelRenderer.render(scene, camera);
}

// Recursively load all .cfg files and image files from a user-selected directory
async function loadCfgFilesRecursively() {
    const planetConfigs = [];
    const iconPaths = {};

    async function readDirectory(dirHandle) {
        for await (const entry of dirHandle.values()) {
            if (entry.kind === 'file') {
                if (entry.name.endsWith('.cfg')) {
                    const file = await entry.getFile();
                    const text = await file.text();
                    if (text.trimStart().startsWith('@Kopernicus:AFTER[Kopernicus]\n{\n    Body')) {
                        planetConfigs.push({ name: entry.name, content: text });
                    }
                }
                if (/\.(png|jpg|jpeg|gif|webp)$/i.test(entry.name)) {
                    const file = await entry.getFile();
                    iconPaths[entry.name] = URL.createObjectURL(file);
                }
            } else if (entry.kind === 'directory') {
                await readDirectory(entry);
            }
        }
    }

    try {
        const dirHandle = await window.showDirectoryPicker();
        await readDirectory(dirHandle);
        console.log('Loaded CFG files:', planetConfigs);
        return { planetConfigs, iconPaths };
    } catch (err) {
        console.error('Error reading directory:', err);
        return { planetConfigs: [], iconPaths: {} };
    }
}