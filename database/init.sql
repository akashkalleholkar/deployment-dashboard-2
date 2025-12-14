
CREATE TABLE IF NOT EXISTS projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  active TINYINT(1) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS environments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS deployments (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  environment_id INT NOT NULL,
  deployed_at DATETIME NOT NULL,
  build_id VARCHAR(255),
  status ENUM('success','failed','in_progress') DEFAULT 'success',
  actor VARCHAR(255),
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (environment_id) REFERENCES environments(id),
  INDEX idx_deployments_proj_env_date (project_id, environment_id, deployed_at)
);

INSERT IGNORE INTO environments (name) VALUES ('prod'), ('uat'), ('dev');
INSERT IGNORE INTO projects (name, active) VALUES ('Payments', 1), ('Orders', 1), ('Auth', 1), ('Inventory', 1);
