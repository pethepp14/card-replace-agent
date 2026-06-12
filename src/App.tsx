import { useMemo, useState } from 'react';

type Reason = 'broken' | 'stolen' | 'damaged';

const reasons: { value: Reason; label: string; text: string }[] = [
  {
    value: 'broken',
    label: 'Broken Card',
    text: 'Chip or magnetic strip is not working, or the card is physically cracked.',
  },
  {
    value: 'stolen',
    label: 'Stolen Card',
    text: 'Card was lost or taken and should be frozen immediately and replaced.',
  },
  {
    value: 'damaged',
    label: 'Damaged Card',
    text: 'Card is bent, melted, or otherwise unusable at ATMs or point-of-sale terminals.',
  },
];

export default function App() {
  const [selectedReason, setSelectedReason] = useState<Reason>('broken');
  const [submitted, setSubmitted] = useState(false);

  const selectedCase = useMemo(
    () => reasons.find((item) => item.value === selectedReason) ?? reasons[0],
    [selectedReason],
  );

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <main className="app-shell">
      <section className="hero-card">
        <p className="eyebrow">Card Replace Agent</p>
        <h1>Start a replacement request in minutes.</h1>
        <p className="lede">
          This assistant helps customers report broken, stolen, or damaged cards and prepares a
          clear request summary for the support team.
        </p>
      </section>

      <section className="panel-grid">
        <article className="panel">
          <h2>Choose the issue</h2>
          <div className="reason-list">
            {reasons.map((item) => (
              <button
                key={item.value}
                type="button"
                className={`reason-card ${selectedReason === item.value ? 'active' : ''}`}
                onClick={() => setSelectedReason(item.value)}
              >
                <strong>{item.label}</strong>
                <span>{item.text}</span>
              </button>
            ))}
          </div>
        </article>

        <article className="panel request-panel">
          <h2>Replacement request</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Full name
              <input type="text" placeholder="Alex Morgan" required />
            </label>
            <label>
              Card number (last 4 digits)
              <input type="text" placeholder="4821" maxLength={4} required />
            </label>
            <label>
              Email
              <input type="email" placeholder="alex@example.com" required />
            </label>
            <label>
              Brief notes
              <textarea
                rows={4}
                placeholder={`Describe what happened with your ${selectedCase.label.toLowerCase()} card.`}
              />
            </label>
            <button type="submit" className="submit-btn">Submit replacement request</button>
          </form>

          {submitted && (
            <div className="confirmation-box" role="status">
              <strong>Request received.</strong>
              <p>
                We’ve flagged your case as <em>{selectedCase.label}</em>. A support agent will review
                the request and guide you through the replacement steps.
              </p>
            </div>
          )}
        </article>
      </section>
    </main>
  );
}
