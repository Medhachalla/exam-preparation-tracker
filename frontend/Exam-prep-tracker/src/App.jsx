import { useEffect, useState } from "react";
import { api } from "./api";

const renderWithLinks = text => {
  const urlRegex = /(https?:\/\/[^\s]+)/g;

  return text.split(urlRegex).map((part, index) =>
    urlRegex.test(part) ? (
      <a
        key={index}
        href={part}
        target="_blank"
        rel="noreferrer"
        className="text-indigo-600 underline break-all"
      >
        {part}
      </a>
    ) : (
      <span key={index}>{part}</span>
    )
  );
};


function App() {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [units, setUnits] = useState([]);
  const [selectedUnit, setSelectedUnit] = useState(null);
  const [topics, setTopics] = useState([]);

  const [newSubject, setNewSubject] = useState("");
  const [newUnit, setNewUnit] = useState("");
  const [newTopic, setNewTopic] = useState("");

  
  const [notes, setNotes] = useState([]);
  const [noteText, setNoteText] = useState("");
  const [unitProgress, setUnitProgress] = useState(0);
  const [subjectProgress, setSubjectProgress] = useState(0);


  useEffect(() => {
    api.get("/subjects").then(res => setSubjects(res.data));
  }, []);

  const loadUnits = subject => {
  setSelectedSubject(subject);
  setSelectedUnit(null);
  setUnits([]);
  setTopics([]);
  setNotes([]);
  setUnitProgress(0);

  api.get(`/subjects/${subject.id}/units`).then(res => setUnits(res.data));
  api.get(`/subjects/${subject.id}/progress`).then(res => setSubjectProgress(res.data.progress));
};


  const loadTopics = unit => {
  setSelectedUnit(unit);
  setTopics([]);
  setNotes([]);
  setUnitProgress(0);

  api.get(`/units/${unit.id}/topics`).then(res => setTopics(res.data));
  api.get(`/units/${unit.id}/notes`).then(res => setNotes(res.data));
  api.get(`/units/${unit.id}/progress`).then(res => setUnitProgress(res.data.progress));
};


  const addSubject = () => {
    if (!newSubject.trim()) return;
    api.post("/subjects", { name: newSubject }).then(res => {
      setSubjects(prev => [...prev, res.data]);
      setNewSubject("");
    });
  };

  const addUnit = () => {
    if (!newUnit.trim() || !selectedSubject) return;
    api.post(`/subjects/${selectedSubject.id}/units`, { name: newUnit }).then(res => {
      setUnits(prev => [...prev, res.data]);
      setNewUnit("");
    });
  };

  const addTopic = () => {
    if (!newTopic.trim() || !selectedUnit) return;
    api.post(`/units/${selectedUnit.id}/topics`, { name: newTopic }).then(res => {
      setTopics(prev => [...prev, res.data]);
      setNewTopic("");
    });
  };

  const toggleTopic = topic => {
  const newStatus = topic.status === "Completed"
    ? "Not Started"
    : "Completed";

  api.put(`/topics/${topic.id}/status`, { status: newStatus })
    .then(() => {
      setTopics(prev =>
        prev.map(t =>
          t.id === topic.id ? { ...t, status: newStatus } : t
        )
      );

      api
        .get(`/units/${selectedUnit.id}/progress`)
        .then(res => setUnitProgress(res.data.progress));

      api
        .get(`/subjects/${selectedSubject.id}/progress`)
        .then(res => setSubjectProgress(res.data.progress));
    });
};

  const toggleUnit = checked => {
  const status = checked ? "Completed" : "Not Started";

  Promise.all(
    topics.map(t =>
      api.put(`/topics/${t.id}/status`, { status })
    )
  ).then(() => {
    setTopics(prev =>
      prev.map(t => ({ ...t, status }))
    );

    api
      .get(`/units/${selectedUnit.id}/progress`)
      .then(res => setUnitProgress(res.data.progress));

    api
      .get(`/subjects/${selectedSubject.id}/progress`)
      .then(res => setSubjectProgress(res.data.progress));
  });
};


  const deleteSubject = id => {
    api.delete(`/subjects/${id}`).then(() => {
      setSubjects(prev => prev.filter(s => s.id !== id));
      setSelectedSubject(null);
      setUnits([]);
      setTopics([]);
      setNotes([]);
    });
  };

  const deleteUnit = id => {
    api.delete(`/units/${id}`).then(() => {
      setUnits(prev => prev.filter(u => u.id !== id));
      setSelectedUnit(null);
      setTopics([]);
      setNotes([]);
    });
  };

  const deleteTopic = id => {
    api.delete(`/topics/${id}`).then(() => {
      setTopics(prev => prev.filter(t => t.id !== id));
    });
  };

  
  const addNote = () => {
    if (!noteText.trim()) return;

    api.post(`/units/${selectedUnit.id}/notes`, {
      content: noteText
    }).then(res => {
      setNotes(prev => [res.data, ...prev]);
      setNoteText("");
    });
  };

  const deleteNote = id => {
    api.delete(`/notes/${id}`).then(() => {
      setNotes(prev => prev.filter(n => n.id !== id));
    });
  };

  const completedCount = topics.filter(t => t.status === "Completed").length;
  const progressPercent = topics.length
    ? Math.round((completedCount / topics.length) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-300 to-indigo-400 p-10">
      <h1 className="text-center text-4xl font-bold text-white mb-8 tracking-wide">
        Exam Preparation Tracker
      </h1>

      
      <div className="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl p-8 space-y-10">
        <section>
          <h2 className="text-xl font-semibold mb-4">Subjects</h2>

          <div className="flex gap-3 mb-4">
            <input
              className="flex-1 border rounded-lg px-3 py-2"
              placeholder="New subject"
              value={newSubject}
              onChange={e => setNewSubject(e.target.value)}
            />
            <button
              onClick={addSubject}
              className="bg-indigo-500 text-white px-4 rounded-lg"
            >
              Add
            </button>
          </div>

          <ul className="space-y-2">
            {subjects.map(s => (
              <li
                key={s.id}
                className={`flex justify-between items-center p-3 rounded-lg cursor-pointer ${
                  selectedSubject?.id === s.id
                    ? "bg-indigo-100 font-semibold"
                    : "hover:bg-slate-100"
                }`}
                onClick={() => loadUnits(s)}
              >
                {s.name}
                <button onClick={() => deleteSubject(s.id)}>✕</button>
              </li>
            ))}
          </ul>
        </section>

        {selectedSubject && (
          <div className="grid grid-cols-2 gap-10">
            <section>
              <div className="mb-6">
              <p className="text-sm font-medium text-slate-600 mb-1">
                Subject Progress
              </p>

              <div className="h-3 bg-slate-200 rounded">
                <div
                  className="h-full bg-indigo-600 rounded transition-all duration-300"
                  style={{ width: `${subjectProgress}%` }}
                />
              </div>
              </div>

              <h3 className="font-semibold mb-3">Units</h3>

              <div className="flex gap-2 mb-3">
                <input
                  className="flex-1 border rounded px-2 py-1"
                  placeholder="New unit"
                  value={newUnit}
                  onChange={e => setNewUnit(e.target.value)}
                />
                <button onClick={addUnit}>Add</button>
              </div>

              <ul className="space-y-2">
                {units.map(u => (
                  <li
                    key={u.id}
                    className={`flex justify-between p-2 rounded cursor-pointer ${
                      selectedUnit?.id === u.id
                        ? "bg-blue-100"
                        : "hover:bg-slate-100"
                    }`}
                    onClick={() => loadTopics(u)}
                  >
                    {u.name}
                    <button onClick={() => deleteUnit(u.id)}>✕</button>
                  </li>
                ))}
              </ul>
            </section>

            {selectedUnit && (
              <section>
                <h3 className="font-semibold mb-3">Topics</h3>

                <div className="flex gap-2 mb-3">
                  <input
                    className="flex-1 border rounded px-2 py-1"
                    placeholder="New topic"
                    value={newTopic}
                    onChange={e => setNewTopic(e.target.value)}
                  />
                  <button onClick={addTopic}>Add</button>
                </div>

                <div className="mb-3">
                  <input
                    type="checkbox"
                    checked={topics.length && completedCount === topics.length}
                    onChange={e => toggleUnit(e.target.checked)}
                  />{" "}
                  Mark unit complete
                </div>

                <div className="h-2 bg-slate-200 rounded mb-4">
                  <div className="h-2 bg-slate-200 rounded mb-4">
                    <div
                      className="h-full bg-indigo-500 rounded transition-all"
                      style={{ width: `${unitProgress}%` }}
                    />
                  </div>
                </div>

                <ul className="space-y-2">
                  {topics.map(t => (
                    <li key={t.id} className="flex justify-between items-center">
                      <label className="flex gap-2 items-center">
                        <input
                          type="checkbox"
                          checked={t.status === "Completed"}
                          onChange={() => toggleTopic(t)}
                        />
                        {t.name}
                      </label>
                      <button onClick={() => deleteTopic(t.id)}>✕</button>
                    </li>
                  ))}
                </ul>
              </section>
            )}
          </div>
        )}
      </div>

      
      {selectedUnit && (
        <div className="max-w-6xl mx-auto mt-10 bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-semibold mb-4">
            Notebook – {selectedUnit.name}
          </h2>

          <textarea
            className="w-full min-h-[140px] border rounded-lg p-3 mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            placeholder="Write notes, paste links, explanations, formulas..."
            value={noteText}
            onChange={e => setNoteText(e.target.value)}
          />

          <div className="flex justify-end mb-6">
            <button
              onClick={addNote}
              className="bg-indigo-500 text-white px-5 py-2 rounded-lg hover:bg-indigo-600"
            >
              Add Note
            </button>
          </div>

          <div className="space-y-4">
            {notes.map(n => (
              <div
                key={n.id}
                className="relative bg-slate-50 border rounded-lg p-4"
              >
                <button
                  onClick={() => deleteNote(n.id)}
                  className="absolute top-2 right-2 text-red-500"
                >
                  ✕
                </button>

                <div className="whitespace-pre-wrap text-sm font-sans leading-relaxed">
                  {renderWithLinks(n.content)}
                </div>

              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
