/**
 * Отображает текущее состояние сущности в виде цветного бейджа.
 * @param {{ status: string }} props
 * @returns {JSX.Element}
 */
function StatusBadge({ status }) {
  return <span className={`status-chip status-${status.toLowerCase()}`}>{status}</span>;
}

/**
 * Унифицированный переключатель для ВМ и интерфейсов.
 * @param {{ checked: boolean, onChange: () => void }} props
 * @returns {JSX.Element}
 */
function ToggleSwitch({ checked, onChange }) {
  return (
    <button
      aria-label={checked ? "Выключить" : "Включить"}
      className={`toggle-switch ${checked ? "toggle-switch-on" : ""}`}
      onClick={onChange}
      type="button"
    >
      <span className="toggle-switch-track">
        <span className="toggle-switch-thumb" />
      </span>
      <span className="toggle-switch-label">{checked ? "ON" : "OFF"}</span>
    </button>
  );
}

/**
 * Универсальная панель отображения карточек ВМ и интерфейсов.
 * @param {{
 *   title: string,
 *   caption: string,
 *   items: Array<Record<string, any>>,
 *   type: "vm" | "interface",
 *   onToggle: (id: number, nextStatus: string) => void,
 *   onDelete?: (id: number) => void
 * }} props
 * @returns {JSX.Element}
 */
export function InventoryPanel({ title, caption, items, type, onToggle, onDelete }) {
  return (
    <section className="panel inventory-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">{caption}</p>
          <h2>{title}</h2>
        </div>
      </div>

      <div className="inventory-grid">
        {items.map((item) => {
          const isEnabled = type === "vm" ? item.status === "running" : item.status === "up";
          const nextStatus =
            type === "vm" ? (isEnabled ? "stopped" : "running") : isEnabled ? "down" : "up";

          return (
            <article className="inventory-card" key={item.id}>
              <div className="inventory-card-top">
                <div>
                  <h3>{item.name}</h3>
                  <p className="muted">ID: {item.id}</p>
                </div>
                <StatusBadge status={item.status} />
              </div>

              <div className="meta-list">
                <p>Создано: {new Date(item.createdAt).toLocaleString("ru-RU")}</p>
                {"networkIds" in item ? <p>Сети: {item.networkIds.join(", ") || "нет"}</p> : null}
                {"vmId" in item ? <p>ВМ: {item.vmId}</p> : null}
                {"networkId" in item ? <p>Сеть: {item.networkId}</p> : null}
              </div>

              <div className="card-actions">
                <ToggleSwitch checked={isEnabled} onChange={() => onToggle(item.id, nextStatus)} />
                {type === "vm" ? (
                  <button className="danger-button" onClick={() => onDelete?.(item.id)} type="button">
                    Удалить
                  </button>
                ) : (
                  <button className="danger-button" disabled type="button">
                    Удалить
                  </button>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
