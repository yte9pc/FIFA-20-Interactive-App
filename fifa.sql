CREATE TABLE country
        ( country_name VARCHAR(30),
          continent VARCHAR(2),
		  PRIMARY KEY (country_name)
		  );
          
CREATE TABLE club
        ( club_name VARCHAR(30),
          league_name VARCHAR(30), 
          PRIMARY KEY (club_name)
		  ); 

CREATE TABLE position
        ( position VARCHAR(3),
          description VARCHAR(30),
          position_group VARCHAR(15),
		  PRIMARY KEY (position)
		  );

CREATE TABLE player
        ( player_id INT,
		  player_name VARCHAR(30),
          country_name VARCHAR(30),
		  PRIMARY KEY (player_id),
          FOREIGN KEY (country_name) REFERENCES country
          );  

CREATE TABLE stat
        ( player_id INT,
          overall_rating INT,
          skill INT,
          weak_foot INT,
          work_rate VARCHAR(5),
          pace INT,
          shooting INT,
          passing INT,
          dribbling INT,
          defending INT,
          physicality INT,
          height INT,
		  PRIMARY KEY (player_id)
		  );
          
CREATE TABLE player_club
        ( player_id INT,
		  club_name VARCHAR(30),
          salary NUMERIC(8,2),
          contract_length NUMERIC(4,2), 
		  PRIMARY KEY (player_id)
		  FOREIGN KEY (club_name) REFERENCES club
		  );

CREATE TABLE player_position
  	   ( player_id INT,
		 position VARCHAR(3),
		 PRIMARY KEY (player_id, position)
		  );  

CREATE TABLE club_country
	   ( club_name VARCHAR(30),
		 country_name VARCHAR(30),
		 PRIMARY KEY (club_name),
		 FOREIGN KEY (country_name) REFERENCES country
		  ); 