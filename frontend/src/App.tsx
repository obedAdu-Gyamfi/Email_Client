import React, { useState } from "react";

export default function EmailSender() {
  const [form, setForm] = useState({
    sender: "",
    receiver: "",
    subject: "",
    body: "",
    cc: "",
    bcc: "",
  });

  const [attachments, setAttachments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleFileChange(e) {
    setAttachments([...e.target.files]);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const formData = new FormData();

    formData.append("sender ", form.sender);
    formData.append("receiver ", form.receiver);
    formData.append("subject ", form.subject);
    formData.append("body ", form.body);
    formData.append("cc ", form.cc);
    formData.append("bcc ", form.bcc);

    attachments.forEach((file) => {
      formData.append("attachments ", file);
    });

    try {
      const res = await fetch("http://127.0.0.1:8000/send-email", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setResult("Error: " + err.message);
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex justify-center">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 text-center">
          SMTP Email Sender
        </h1>

        <form className="space-y-4" onSubmit={handleSubmit}>
          {Object.keys(form).map((key) => (
            <div key={key}>
              <label className="block font-semibold mb-1 capitalize">{key}</label>
              <input
                type="text"
                name={key}
                value={form[key]}
                onChange={handleChange}
                className="w-full p-2 border rounded-lg"
              />
            </div>
          ))}

          <div>
            <label className="block font-semibold mb-1">Attachments</label>
            <input
              type="file"
              multiple
              onChange={handleFileChange}
              className="w-full p-2 border rounded-lg"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl font-bold"
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Email"}
          </button>
        </form>

        {result && (
          <pre className="mt-6 bg-gray-900 text-green-400 p-4 rounded-xl text-sm overflow-auto">
            {result}
          </pre>
        )}
      </div>
    </div>
  );
}
