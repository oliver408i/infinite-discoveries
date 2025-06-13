import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { DDSLoader } from 'three/addons/loaders/DDSLoader.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.001, 10000 );

const SCALE_FACTOR = 0.00000001;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize( window.innerWidth, window.innerHeight );

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
labelRenderer.domElement.style.pointerEvents = 'none';

const controls = new OrbitControls( camera, renderer.domElement );
const ddsLoader = new DDSLoader();

camera.position.z = 5;

function parseCfgValues(text) {
    const result = {};
    const lines = text.split('\n');
    for (let line of lines) {
        line = line.trim();
        if (line.startsWith('//') || !line.includes('=')) continue;
        const [key, value] = line.split('=').map(s => s.trim());
        if (!(key in result)) {
            result[key] = value;
        }
    }
    return result;
}

function buildBodyTree(configs) {
    const bodies = {};
    const children = {};

    for (const cfg of configs) {
        const values = parseCfgValues(cfg.content);
        const internalName = values.name;
        // Remove ^N from displayName and internalName for displayName
        const displayName = (values.displayName || internalName).replace(/\^N/g, '');
        const referenceBody = values.referenceBody || 'Sun';
        const radius = parseFloat(values.radius || '1000');
        const semiMajorAxis = parseFloat(values.semiMajorAxis || '0');
        const eccentricity = parseFloat(values.eccentricity || '0');
        const inclination = parseFloat(values.inclination || '0');
        const Tag = values.Tag

        bodies[internalName] = {
            name: displayName,
            internalName,
            displayName,
            referenceBody,
            radius,
            semiMajorAxis,
            eccentricity,
            inclination,
            Tag,
            sunlightColor: values.sunlightColor || null,
            luminosity: values.luminosity ? parseFloat(values.luminosity) : null,
            type: values.type || null,
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

// Move main loading logic into a new async function
async function initializeScene(data) {
    const { planetConfigs, iconPaths, ddsPaths } = data;
    
    document.getElementById('loading').innerText = "Loading celestial bodies...";
    
    console.log('Loaded CFG files:', planetConfigs);
    console.log(`Total configs loaded: ${planetConfigs.length}`);

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

    async function addBodiesToScene(bodies, parentPosition = new THREE.Vector3(0, 0, 0), visited = new Set(), textureBasePathMap) {
        const orbitSpacing = 0.05;

        for (const body of bodies) {
            if (visited.has(body.internalName)) {
                console.warn(`Skipping already visited body: ${body.name} (${body.internalName})`);
                continue; // Prevent cycles
            }
            visited.add(body.internalName);
            // Skip sphere creation for barycenter
            if (body.Tag === 'InfD_Barycenter') {
                console.log(`Skipping sphere creation for barycenter: ${body.name}`);
                if (body.children.length > 0) {
                    console.log(`Adding children of barycenter ${body.name}: ${body.children.map(c => c.name).join(', ')}`);
                    await addBodiesToScene(body.children, parentPosition, visited, textureBasePathMap);
                }
                continue;
            }
            console.log(`Placing body: ${body.name}, semiMajorAxis: ${body.semiMajorAxis}, radius: ${body.radius}`, body);

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

            // Dynamically determine geometry resolution based on eccentricity and radius
            let widthSegments = 16;
            let heightSegments = 16;

            if (body.eccentricity < 0.01) {
                widthSegments = 32;
                heightSegments = 32;
            }

            if (body.radius < 1000000) {
                widthSegments = Math.max(widthSegments, 64);
                heightSegments = Math.max(heightSegments, 64);
            }

            const geometry = new THREE.SphereGeometry(body.radius * SCALE_FACTOR, widthSegments, heightSegments);
            const isStar = body.type === 'Star';
            const material = new THREE.MeshStandardMaterial({
                color: 0xffffff,
                transparent: isStar,
                opacity: isStar ? 0.2 : 1.0,
                depthWrite: !isStar,
                emissive: isStar ? new THREE.Color(0, 0, 0) : new THREE.Color(0, 0, 0),
                emissiveIntensity: isStar ? 1.5 : 0
            });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.copy(position);
            mesh.userData = { name: body.name };
            scene.add(mesh);

            // Parse config values for texture/normal/heightmap file names
            const cfg = planetConfigs.find(cfg => parseCfgValues(cfg.content).name === body.internalName);
            let values = null;
            if (cfg) {
                values = parseCfgValues(cfg.content);
            }
            // Parse VertexHeightMap block for heightmap name
            let heightmapName = null;
            if (cfg && cfg.content.includes('VertexHeightMap')) {
                const lines = cfg.content.split('\n').map(line => line.trim());
                let insideBlock = false;
                for (let line of lines) {
                    if (line.startsWith('VertexHeightMap')) {
                        insideBlock = true;
                        continue;
                    }
                    if (insideBlock && line.startsWith('map')) {
                        heightmapName = line.split('=')[1].trim().split('/').pop();
                        break;
                    }
                    if (insideBlock && line === '}') break;
                }
            }
            if (heightmapName && ddsPaths[heightmapName]) {
                console.log(`Found heightmap for ${body.name}: ${heightmapName}`);
                try {
                    const texture = await new Promise((resolve, reject) => {
                        ddsLoader.load(ddsPaths[heightmapName], resolve, undefined, reject);
                    });
                    if (texture && texture.image && texture.image.width && texture.image.height) {
                        material.displacementMap = texture;
                        texture.wrapS = THREE.RepeatWrapping;
                        texture.wrapT = THREE.RepeatWrapping;
                        material.displacementScale = body.radius < 1000000
                            ? body.radius * SCALE_FACTOR * 0.05
                            : body.radius * SCALE_FACTOR * 0.15;
                        material.needsUpdate = true;
                    } else {
                        console.warn(`Displacement map for ${body.name} is invalid or incomplete`, texture);
                    }
                } catch (error) {
                    console.error(`Failed to load heightmap for ${body.name}:`, error);
                }
            } else {
                console.log(`No heightmap found for ${body.name}`);
            }

            const colormapName = values && values.texture ? values.texture.split('/').pop() : `${body.internalName}_CLR.dds`;
            if (ddsPaths[colormapName]) {
                console.log(`Found color map for ${body.name}: ${colormapName}`);
                try {
                    const colorTexture = await new Promise((resolve, reject) => {
                        ddsLoader.load(ddsPaths[colormapName], resolve, undefined, reject);
                    });
                    if (colorTexture && colorTexture.image && colorTexture.image.width && colorTexture.image.height) {
                        material.map = colorTexture;
                        colorTexture.wrapS = THREE.RepeatWrapping;
                        colorTexture.wrapT = THREE.RepeatWrapping;
                        material.needsUpdate = true;
                    } else {
                        console.warn(`Color map for ${body.name} is invalid or incomplete`, colorTexture);
                    }
                } catch (error) {
                    console.error(`Failed to load color map for ${body.name}:`, error);
                }
            } else {
                console.log(`No color map found for ${body.name}`);
            }

            // Load normal map if present (shader decode for DXT5_NM)
            const normalmapName = values && values.normals ? values.normals.split('/').pop() : `${body.internalName}_NRM.dds`;
            if (ddsPaths[normalmapName]) {
                console.log(`Found normal map for ${body.name}: ${normalmapName}`);
                try {
                    const rawTexture = await new Promise((resolve, reject) => {
                        ddsLoader.load(ddsPaths[normalmapName], resolve, undefined, reject);
                    });
                    if (rawTexture && rawTexture.image && rawTexture.image.width && rawTexture.image.height) {
                        material.normalMap = rawTexture;
                        material.normalScale = body.radius < 1000000
                            ? new THREE.Vector2(1.5, 1.5)
                            : new THREE.Vector2(1, 1);
                        material.needsUpdate = true;
                    } else {
                        console.warn(`Normal map for ${body.name} is invalid or incomplete`, rawTexture);
                    }
                } catch (error) {
                    console.error(`Failed to load normal map for ${body.name}:`, error);
                }
            } else {
                console.log(`No normal map found for ${body.name}`);
            }

            // Enhanced star rendering: halo, light, and emissive material for InfD_Star
            if (isStar) {
                console.log("Adding halo, light, and emissive texture for star:", body.internalName);

                // Add emissive color dynamically based on sunlightColor if present
                let emissiveColor = new THREE.Color(1, 1, 1);
                if (body.sunlightColor) {
                    const parts = body.sunlightColor.split(',').slice(0, 3).map(Number);
                    if (parts.length === 3) {
                        emissiveColor = new THREE.Color(parts[0], parts[1], parts[2]);
                    }
                }
                material.emissive = emissiveColor;
                material.emissiveIntensity = 5;
                material.needsUpdate = true;

                // Add halo mesh
                const haloGeometry = new THREE.SphereGeometry(body.radius * SCALE_FACTOR * 1.1, 50, 50);
                const haloMaterial = new THREE.ShaderMaterial({
                    uniforms: {
                        HINTENSITY: { value: body.luminosity ? Math.sqrt(body.luminosity) * 0.01 : 1.0 }
                    },
                    vertexShader: `varying vec3 vertexNormal;
                        void main() {
                            vertexNormal = normal;
                            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                        }`,
                    fragmentShader: `uniform float HINTENSITY;
                        varying vec3 vertexNormal;
                        void main() {
                            float intensity = pow(0.9 - dot(vertexNormal, vec3(0, 0, 1.0)), 2.0) * HINTENSITY;
                            gl_FragColor = vec4(0.8, 1.0, 0.6, 0.2) * intensity;
                        }`,
                    blending: THREE.AdditiveBlending,
                    side: THREE.BackSide,
                    transparent: true,
                    depthWrite: false
                });
                const halo = new THREE.Mesh(haloGeometry, haloMaterial);
                halo.position.copy(position);
                scene.add(halo);

                // Add sunlight PointLight
                let intensity = 10;
                if (body.luminosity !== null && !isNaN(body.luminosity)) {
                    intensity = body.luminosity / 10;
                }
                const light = new THREE.PointLight(emissiveColor, intensity, 5000, 1);
                light.position.copy(position);
                scene.add(light);
            }

            displayedBodyCount++;

            if (distance > 0) {
                const orbitLine = createOrbitLine(distance, body.eccentricity || 0, body.inclination || 0);
                orbitLine.position.copy(parentPosition);
                scene.add(orbitLine);
            }

            bodyMeshes.push(mesh);

            const labelDiv = document.createElement('div');
            labelDiv.className = 'label';
            // Show both displayName and internalName
            labelDiv.innerHTML = `<div style="font-weight: bold;">${body.name}</div><div style="font-size: 10px; opacity: 0.7;">${body.internalName}</div>`;
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
                currentFocus = bodyMeshes.indexOf(mesh);
            });

            const label = new CSS2DObject(labelDiv);
            const labelYOffset = body.radius * SCALE_FACTOR * 0.8 + 0.05;
            label.position.set(0, labelYOffset, 0);
            mesh.add(label);

            // Add icon as CSS2DRenderer icon instead of sprite
            if (!cfg) {
                console.warn(`No matching config found for body: ${body.name} (${body.internalName})`);
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
                    const iconYOffset = body.radius * SCALE_FACTOR * 0.9 + 0.15;
                    iconLabel.position.set(0, iconYOffset, 0);
                    mesh.add(iconLabel);
                } else {
                    console.warn(`Icon file not found for body: ${body.name}, icon: ${iconFileName}`);
                }
            }

            // Add ring if specified (key-based scan, no regex)
            if (values && cfg && cfg.content.includes('Rings')) {
                const lines = cfg.content.split('\n').map(line => line.trim());
                let innerRadius, outerRadius, ringColor, ringTexture;
                for (let line of lines) {
                    if (line.startsWith('innerRadius')) innerRadius = parseFloat(line.split('=')[1].trim());
                    if (line.startsWith('outerRadius')) outerRadius = parseFloat(line.split('=')[1].trim());
                    if (line.startsWith('color')) ringColor = line.split('=')[1].trim().split(',').slice(0, 3).map(parseFloat);
                    if (line.startsWith('texture')) ringTexture = line.split('=')[1].trim().split('/').pop();
                }

                if (innerRadius && outerRadius && ringTexture) {
                    // Calculate ring distances from the surface of the planet sphere
                    const planetRadius = body.radius * SCALE_FACTOR;
                    const inner = planetRadius + (innerRadius * SCALE_FACTOR);
                    const outer = planetRadius + (outerRadius * SCALE_FACTOR);
                    // const textureUrl = iconPaths[ringTexture]; // Not needed for debug version

                    const ringGeometry = new THREE.RingGeometry(inner, outer, 128);
                    // Debug: solid magenta, no texture, semi-transparent
                    const ringMaterial = new THREE.MeshBasicMaterial({
                        color: 0xff00ff, // bright magenta for debugging visibility
                        side: THREE.DoubleSide,
                        transparent: true,
                        opacity: 0.6,
                        depthWrite: false
                    });
                    const ringMesh = new THREE.Mesh(ringGeometry, ringMaterial);
                    const inclinationRad = THREE.MathUtils.degToRad(body.inclination || 0);
                    const nodeRad = THREE.MathUtils.degToRad(parseFloat(values?.longitudeOfAscendingNode || 0));

                    ringMesh.rotation.set(0, 0, 0);
                    ringMesh.rotation.order = 'ZYX';
                    ringMesh.rotateZ(nodeRad);
                    ringMesh.rotateX(inclinationRad);
                    ringMesh.position.copy(position);
                    //scene.add(ringMesh); // TODO: Fix rings
                    console.log(`Added ring for body: ${body.name} with radius: ${inner} to ${outer} (sphere radius ${planetRadius})`);
                }
            }

            if (body.children.length > 0) {
                console.log(`Adding children of ${body.name}: ${body.children.map(c => c.name).join(', ')}`);
                await addBodiesToScene(body.children, position, visited, textureBasePathMap);
            } else {
                console.log(`Body ${body.name} has no children.`);
            }
        }
    }

    await addBodiesToScene(system, new THREE.Vector3(0, 0, 0), new Set(), textureBasePathMap);
    console.log(`Displayed total bodies: ${displayedBodyCount}`);

    // Focus camera on the first body after all bodies are added
    if (bodyMeshes.length > 0) {
        const target = bodyMeshes[0].position;
        const offset = new THREE.Vector3(0, 0, bodyMeshes[0].geometry.parameters.radius * SCALE_FACTOR * 10 + 1);
        camera.position.copy(target.clone().add(offset));
        controls.target.copy(target);
    }

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            if (bodyMeshes.length === 0) return;
            if (e.shiftKey) {
                currentFocus = (currentFocus - 1 + bodyMeshes.length) % bodyMeshes.length;
            } else {
                currentFocus = (currentFocus + 1) % bodyMeshes.length;
            }
            const target = bodyMeshes[currentFocus].position;
            const body = bodyMeshes[currentFocus];
            const offset = new THREE.Vector3(0, 0, body.geometry.parameters.radius * SCALE_FACTOR * 10 + 1);
            camera.position.copy(target.clone().add(offset));
            controls.target.copy(target);
        }
    });

    document.getElementById('loading').remove();
    document.body.style.overflow = 'hidden';
    document.body.appendChild( renderer.domElement );
    document.body.appendChild(labelRenderer.domElement);

    animate();
}

function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
    labelRenderer.render(scene, camera);
}


// Load .cfg, .dds, and image files from a zip file
async function loadCfgFromZip(file) {

    document.getElementById('inputs').remove()
    const loadingText = document.createElement('div');
    loadingText.id = 'loading';
    loadingText.innerText = 'Unzipping...';
    loadingText.style.position = 'absolute';
    loadingText.style.top = '50%';
    loadingText.style.left = '50%';
    loadingText.style.transform = 'translate(-50%, -50%)';
    document.body.appendChild(loadingText);

    const zip = await JSZip.loadAsync(file);
    console.log('Loaded zip file:', zip);

    const planetConfigs = [];
    const iconPaths = {};
    const ddsPaths = {};

    const totalFiles = Object.keys(zip.files).length;

    let filesToLookThrough = totalFiles;
    for (const [path, zipEntry] of Object.entries(zip.files)) {
        if (zipEntry.dir) {
            filesToLookThrough--;
            continue;
        }

        const fileData = await zipEntry.async('blob');
        const fileText = path.endsWith('.cfg') ? await zipEntry.async('text') : null;

        if (path.endsWith('.cfg') && fileText.trimStart().startsWith('@Kopernicus:AFTER[Kopernicus]')) {
            planetConfigs.push({ name: path, content: fileText });
        } else if (/\.(png|jpg|jpeg|gif|webp)$/i.test(path)) {
            iconPaths[path.split('/').pop()] = URL.createObjectURL(fileData);
        } else if (path.toLowerCase().endsWith('.dds')) {
            ddsPaths[path.split('/').pop()] = URL.createObjectURL(fileData);
        }

        filesToLookThrough--;
        loadingText.innerText = `Finding planet configs & textures... (${filesToLookThrough} files left)`;
    }

    return { planetConfigs, iconPaths, ddsPaths };
}

document.getElementById('load-button').addEventListener('click', async () => {
    const fileInput = document.getElementById('zip-upload');
    const file = fileInput.files[0];
    if (!file) {
        alert('No file selected. Please select a zip file.');
        return;
    }

    const { planetConfigs, iconPaths, ddsPaths } = await loadCfgFromZip(file);
    await initializeScene({ planetConfigs, iconPaths, ddsPaths });
});


document.getElementById('zip-upload')?.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const { planetConfigs, iconPaths, ddsPaths } = await loadCfgFromZip(file);
    await initializeScene({ planetConfigs, iconPaths, ddsPaths });
});

window.addEventListener('resize', () => {
    const canvas = renderer.domElement;
    const width = window.innerWidth;
    const height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
    labelRenderer.setSize(width, height);
});
