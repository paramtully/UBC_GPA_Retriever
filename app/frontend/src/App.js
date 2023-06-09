import { useState } from 'react';

function Description() {
  return (
    <div>
      <p>This application uses your login information to retrieve your grade information from ssc and summarizes it in the form of:
        <ol>
          <li>Weighted Average</li>
          <li>GPA (/4.0)</li>
          <li>GPA (/4.33)</li>
        </ol>
      </p>
      <p>You can optionally specify which session to summarize your grade information for in the same form as on ssc (ex 2022W or 2022S). Otherwise it will default to all completed academic sessions.</p>
    </div>
  )
}

function Interactable() {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);

  return (
    <div>
      <Form loading={loading} setLoading={setLoading} setSummary={setSummary} />
      <Result loading={loading} summary={summary} />
    </div>
  );
}

function Form({ loading, setLoading, setSummary }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [session, setSession] = useState('');

  const isSubmittable = username.length && password.length && !loading;

   async function handleSubmit(e) {
    setLoading(true);
    e.preventDefault();

    const data = new FormData();
    data.append('username', username);
    data.append('password', password);
    if (session.length) data.append('session', session);

    let response = null;

    try {
      response = await fetch('/summary', {
        method: 'POST',
        body: data
      });

      response = await response.json();
    } catch (error) {
      response = {error: 'Servers could not be reached...'};
    }

    setSummary(response);
    setLoading(false);
  }

  return (
    <form onSubmit={e => handleSubmit(e)} >
      <input type='text' placeholder='username' value={username} onChange={e => setUsername(e.target.value)} />
      <input type='text' placeholder='password' value={password} onChange={e => setPassword(e.target.value)} />
      <input type='text' placeholder='session' value={session} onChange={e => setSession(e.target.value)} />
      <button disabled={!isSubmittable}>Get Grades</button>
    </form>
  );
}

function Result({loading, summary}) {
  if (!summary && !loading) return <></>;
  else if (loading) return <div>Loading...</div>;
  else if (summary.error !== undefined) return <p style={{color: '#cc0000'}}> {summary.error} </p>;

  return (
    <div>
      <p>Your Grade Summary:</p>
      <p>Average:{" " + summary.average}</p>
      <p>GPA (4.0 Scale):{" " + summary.gpa4}</p>
      <p>GPA (4.33 Scale):{" " + summary.gpa433}</p>
    </div>
  );
}

function App() {
  return (
    <div>
      <h1>UBC Grade Retriever</h1>
      <Description />
      <Interactable />
    </div>
  );
}

export default App;
