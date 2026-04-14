import { useEffect, useState } from "react";

import {
  changeInterfaceStatus,
  changeVirtualMachineStatus,
  createInterface,
  createVirtualMachine,
  deleteVirtualMachine,
  fetchInterfaces,
  fetchNetworks,
  fetchVirtualMachines,
  login,
} from "./api/client";
import { CreateInterfaceForm } from "./components/CreateInterfaceForm";
import { CreateVmForm } from "./components/CreateVmForm";
import { InventoryPanel } from "./components/InventoryPanel";
import { LoginForm } from "./components/LoginForm";


const initialSession = {
  token: "",
  username: "",
};

const sections = [
  { id: "vm-list", label: "Список ВМ" },
  { id: "interface-list", label: "Список интерфейсов" },
  { id: "create", label: "Создание элементов" },
];

/**
 * Основной экран приложения: авторизация, навигация по разделам и синхронизация с backend.
 * @returns {JSX.Element}
 */
export default function App() {
  const [session, setSession] = useState(initialSession);
  const [virtualMachines, setVirtualMachines] = useState([]);
  const [interfaces, setInterfaces] = useState([]);
  const [networks, setNetworks] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [activeSection, setActiveSection] = useState("vm-list");

  /**
   * Обновляет все списки после логина и после любых изменений сущностей.
   * @param {string} token
   * @returns {Promise<void>}
   */
  async function loadInventory(token) {
    const [vmData, interfaceData, networkData] = await Promise.all([
      fetchVirtualMachines(token),
      fetchInterfaces(token),
      fetchNetworks(token),
    ]);

    setVirtualMachines(vmData.items);
    setInterfaces(interfaceData.items);
    setNetworks(networkData.items);
  }

  /**
   * Выполняет логин, сохраняет токен сессии и загружает данные dashboard.
   * @param {{ username: string, password: string }} form
   * @returns {Promise<void>}
   */
  async function handleLogin(form) {
    setError("");
    setIsLoading(true);

    try {
      const data = await login(form);
      const nextSession = {
        token: data.accessToken,
        username: data.username,
      };
      setSession(nextSession);
      await loadInventory(nextSession.token);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  /**
   * Создает ВМ и перечитывает актуальный список.
   * @param {{ name: string }} payload
   * @returns {Promise<void>}
   */
  async function handleCreateVm(payload) {
    await createVirtualMachine(session.token, payload);
    await loadInventory(session.token);
  }

  /**
   * Создает интерфейс и синхронизирует UI с данными БД.
   * @param {{ name: string, vmId: number, networkId: number }} payload
   * @returns {Promise<void>}
   */
  async function handleCreateInterface(payload) {
    await createInterface(session.token, payload);
    await loadInventory(session.token);
  }

  /**
   * Отправляет в backend следующий статус ВМ для toggle-переключателя.
   * @param {number} vmId
   * @param {string} status
   * @returns {Promise<void>}
   */
  async function handleVmToggle(vmId, status) {
    try {
      await changeVirtualMachineStatus(session.token, vmId, status);
      await loadInventory(session.token);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  /**
   * Отправляет в backend следующий статус интерфейса.
   * @param {number} interfaceId
   * @param {string} status
   * @returns {Promise<void>}
   */
  async function handleInterfaceToggle(interfaceId, status) {
    try {
      await changeInterfaceStatus(session.token, interfaceId, status);
      await loadInventory(session.token);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  /**
   * Удаляет ВМ по id и обновляет список после ответа backend.
   * @param {number} vmId
   * @returns {Promise<void>}
   */
  async function handleDeleteVm(vmId) {
    try {
      await deleteVirtualMachine(session.token, vmId);
      await loadInventory(session.token);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  useEffect(() => {
    setError("");
  }, [session.token]);

  /**
   * Полностью очищает локальную сессию и возвращает экран логина.
   * @returns {void}
   */
  function handleLogout() {
    setSession(initialSession);
    setVirtualMachines([]);
    setInterfaces([]);
    setNetworks([]);
    setError("");
    setActiveSection("vm-list");
  }

  if (!session.token) {
    return (
      <main className="app-shell auth-shell">
        <LoginForm error={error} isLoading={isLoading} onSubmit={handleLogin} />
      </main>
    );
  }

  return (
    <main className="app-shell">
      <div className="workspace-layout">
        <aside className="panel sidebar">
          <div className="sidebar-brand">
            <p className="eyebrow">Навигация</p>
            <h2>Управление инфраструктурой</h2>
          </div>

          <nav className="sidebar-nav">
            {sections.map((section) => (
              <button
                key={section.id}
                className={`nav-button ${activeSection === section.id ? "nav-button-active" : ""}`}
                onClick={() => setActiveSection(section.id)}
                type="button"
              >
                {section.label}
              </button>
            ))}
          </nav>
        </aside>

        <section className="main-column">
          <header className="panel topbar">
            <div>
              <p className="eyebrow">Пользователь</p>
              <p className="topbar-username">{session.username}</p>
            </div>
            <button className="secondary-button" onClick={handleLogout} type="button">
              Выйти
            </button>
          </header>

          {error ? <p className="error-text page-error">{error}</p> : null}

          {activeSection === "vm-list" ? (
            <InventoryPanel
              caption="Виртуальные машины"
              items={virtualMachines}
              onDelete={handleDeleteVm}
              onToggle={handleVmToggle}
              title="Список ВМ"
              type="vm"
            />
          ) : null}

          {activeSection === "interface-list" ? (
            <InventoryPanel
              caption="Сетевые интерфейсы"
              items={interfaces}
              onToggle={handleInterfaceToggle}
              title="Список интерфейсов"
              type="interface"
            />
          ) : null}

          {activeSection === "create" ? (
            <section className="forms-layout">
              <CreateVmForm onSubmit={handleCreateVm} />
              <CreateInterfaceForm
                networks={networks}
                onSubmit={handleCreateInterface}
                virtualMachines={virtualMachines}
              />
            </section>
          ) : null}
        </section>
      </div>
    </main>
  );
}
