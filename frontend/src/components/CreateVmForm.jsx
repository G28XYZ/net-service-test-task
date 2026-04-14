import { useState } from "react";


/**
 * Форма создания новой виртуальной машины.
 * @param {{ onSubmit: (payload: { name: string }) => Promise<void> }} props
 * @returns {JSX.Element}
 */
export function CreateVmForm({ onSubmit }) {
  const [name, setName] = useState("");

  /**
   * Не отправляет форму, пока имя ВМ пустое.
   * @param {React.FormEvent<HTMLFormElement>} event
   * @returns {Promise<void>}
   */
  async function handleSubmit(event) {
    event.preventDefault();
    if (!name.trim()) {
      return;
    }

    await onSubmit({ name: name.trim() });
    setName("");
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h2>Создать виртуальную машину</h2>
      </div>
      <label>
        Имя ВМ
        <input
          placeholder="vm-web-01"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
      </label>
      <button className="primary-button" type="submit">
        Создать ВМ
      </button>
    </form>
  );
}
