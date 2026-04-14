import { useState } from "react";


const initialState = {
  username: "admin",
  password: "admin",
};

/**
 * Форма авторизации с демо-учеткой и отображением ошибки входа.
 * @param {{
 *   onSubmit: (form: { username: string, password: string }) => Promise<void>,
 *   error: string,
 *   isLoading: boolean
 * }} props
 * @returns {JSX.Element}
 */
export function LoginForm({ onSubmit, error, isLoading }) {
  const [form, setForm] = useState(initialState);

  /**
   * Обновляет локальное состояние формы по имени поля.
   * @param {React.ChangeEvent<HTMLInputElement>} event
   * @returns {void}
   */
  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  /**
   * Отдает введенные данные родительскому экрану авторизации.
   * @param {React.FormEvent<HTMLFormElement>} event
   * @returns {Promise<void>}
   */
  async function handleSubmit(event) {
    event.preventDefault();
    await onSubmit(form);
  }

  return (
    <form className="panel auth-panel" onSubmit={handleSubmit}>
      <div>
        <p className="eyebrow">Тестовое задание</p>
        <h1>Сервис управления ВМ</h1>
      </div>

      <label>
        Логин
        <input name="username" value={form.username} onChange={handleChange} />
      </label>

      <label>
        Пароль
        <input name="password" type="password" value={form.password} onChange={handleChange} />
      </label>

      {error ? <p className="error-text">{error}</p> : null}

      <button className="primary-button" disabled={isLoading} type="submit">
        {isLoading ? "Вход..." : "Войти"}
      </button>
    </form>
  );
}
