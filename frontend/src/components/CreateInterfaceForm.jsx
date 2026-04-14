import { useState } from "react";


/**
 * Форма создания интерфейса с выбором ВМ и сети.
 * @param {{
 *   virtualMachines: Array<{ id: number, name: string }>,
 *   networks: Array<{ id: number, name: string }>,
 *   onSubmit: (payload: { name: string, vmId: number, networkId: number }) => Promise<void>
 * }} props
 * @returns {JSX.Element}
 */
export function CreateInterfaceForm({ virtualMachines, networks, onSubmit }) {
  const [name, setName] = useState("");
  const [vmId, setVmId] = useState("");
  const [networkId, setNetworkId] = useState("");

  /**
   * Отправляет интерфейс только после выбора ВМ, сети и имени.
   * @param {React.FormEvent<HTMLFormElement>} event
   * @returns {Promise<void>}
   */
  async function handleSubmit(event) {
    event.preventDefault();
    if (!name.trim() || !vmId || !networkId) {
      return;
    }

    await onSubmit({
      name: name.trim(),
      vmId: Number(vmId),
      networkId: Number(networkId),
    });

    setName("");
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h2>Создать интерфейс</h2>
      </div>

      <label>
        Имя интерфейса
        <input
          placeholder="eth2"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
      </label>

      <label>
        Виртуальная машина
        <select value={vmId} onChange={(event) => setVmId(event.target.value)}>
          <option value="">Выберите ВМ</option>
          {virtualMachines.map((vm) => (
            <option key={vm.id} value={vm.id}>
              {vm.name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Сеть
        <select value={networkId} onChange={(event) => setNetworkId(event.target.value)}>
          <option value="">Выберите сеть</option>
          {networks.map((network) => (
            <option key={network.id} value={network.id}>
              {network.name}
            </option>
          ))}
        </select>
      </label>

      <button className="primary-button" type="submit">
        Создать интерфейс
      </button>
    </form>
  );
}
