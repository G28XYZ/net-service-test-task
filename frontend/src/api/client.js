const API_URL = "http://127.0.0.1:8000";

/**
 * Выполняет HTTP-запрос к backend, добавляет Bearer-токен и нормализует ошибки.
 * @param {string} path
 * @param {{
 *   token?: string,
 *   method?: string,
 *   body?: unknown,
 *   headers?: Record<string, string>
 * }} [options]
 * @returns {Promise<any>}
 */
async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
      ...options.headers,
    },
    method: options.method ?? "GET",
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail ?? "Request failed");
  }

  return data;
}

/**
 * Выполняет логин и получает токен текущего пользователя.
 * @param {{ username: string, password: string }} payload
 * @returns {Promise<any>}
 */
export async function login(payload) {
  return request("/auth/login", {
    method: "POST",
    body: payload,
  });
}

/**
 * Загружает список виртуальных машин.
 * @param {string} token
 * @returns {Promise<any>}
 */
export async function fetchVirtualMachines(token) {
  return request("/virtual-machines", { token });
}

/**
 * Создает новую виртуальную машину.
 * @param {string} token
 * @param {{ name: string }} payload
 * @returns {Promise<any>}
 */
export async function createVirtualMachine(token, payload) {
  return request("/virtual-machines", {
    method: "POST",
    token,
    body: payload,
  });
}

/**
 * Отправляет в backend целевое состояние ВМ для toggle-переключателя.
 * @param {string} token
 * @param {number} vmId
 * @param {string} status
 * @returns {Promise<any>}
 */
export async function changeVirtualMachineStatus(token, vmId, status) {
  return request(`/virtual-machines/${vmId}/status`, {
    method: "PATCH",
    token,
    body: { status },
  });
}

/**
 * Удаляет виртуальную машину по id.
 * @param {string} token
 * @param {number} vmId
 * @returns {Promise<any>}
 */
export async function deleteVirtualMachine(token, vmId) {
  return request(`/virtual-machines/${vmId}`, {
    method: "DELETE",
    token,
  });
}

/**
 * Загружает список сетевых интерфейсов.
 * @param {string} token
 * @returns {Promise<any>}
 */
export async function fetchInterfaces(token) {
  return request("/interfaces", { token });
}

/**
 * Создает новый интерфейс с привязкой к ВМ и сети.
 * @param {string} token
 * @param {{ name: string, vmId: number, networkId: number }} payload
 * @returns {Promise<any>}
 */
export async function createInterface(token, payload) {
  return request("/interfaces", {
    method: "POST",
    token,
    body: payload,
  });
}

/**
 * Отправляет в backend целевое состояние интерфейса для toggle-переключателя.
 * @param {string} token
 * @param {number} interfaceId
 * @param {string} status
 * @returns {Promise<any>}
 */
export async function changeInterfaceStatus(token, interfaceId, status) {
  return request(`/interfaces/${interfaceId}/status`, {
    method: "PATCH",
    token,
    body: { status },
  });
}

/**
 * Загружает сети для формы создания интерфейса.
 * @param {string} token
 * @returns {Promise<any>}
 */
export async function fetchNetworks(token) {
  return request("/networks", { token });
}
