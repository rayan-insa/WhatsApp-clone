-- Create the `users` table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the `conversations` table
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- is_group BOOLEAN DEFAULT FALSE
);

-- Create the `messages` table
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(500) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender_id INT NOT NULL,
    conversation_id INT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- Create the `groupchats` table
CREATE TABLE IF NOT EXISTS groupchats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    admin_id INT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the `group_members` association table
CREATE TABLE IF NOT EXISTS group_members (
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groupchats(id) ON DELETE CASCADE
);



-- Insert sample users
INSERT INTO users (username, email) VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com'),
('carol', 'carol@example.com');

-- -- Insert a direct message conversation
-- INSERT INTO conversations (name, is_group) VALUES
-- ('Alice and Bob', FALSE);

-- -- Insert a group chat
-- INSERT INTO conversations (name, is_group) VALUES
-- ('Friends Group', TRUE);

-- Insert group chat details in the groupchats table
INSERT INTO groupchats (name, admin_id) VALUES
('Friends Group', 1);

-- Add members to the group
INSERT INTO group_members (user_id, group_id) VALUES
(1, 1), -- Alice
(2, 1), -- Bob
(3, 1); -- Carol

-- Insert messages
INSERT INTO messages (content, sender_id, conversation_id) VALUES
('Hi Bob!', 1, 1),
('Hey Alice!', 2, 1),
('Welcome to the group!', 1, 2);
