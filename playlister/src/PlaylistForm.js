import React, { useState } from "react";

function PlaylistForm({ onSubmit }) {
  const [description, setDescription] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(description);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Playlist Description:
        <input
          type="text"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
        />
      </label>
      <button type="submit">Generate Playlist</button>
    </form>
  );
}

export default PlaylistForm;
