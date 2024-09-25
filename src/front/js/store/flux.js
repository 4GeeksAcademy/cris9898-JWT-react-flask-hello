const getState = ({ getStore, getActions, setStore }) => {
	return {
	  store: {
		demo: [
		  {
			title: "FIRST",
			background: "white",
			initial: "white",
		  },
		  {
			title: "SECOND",
			background: "white",
			initial: "white",
		  },
		],
	  },
	  actions: {
		register: async (email, password) => {
			try {
			  console.log(email)
			  console.log(password)
			  const response = await fetch(
				process.env.BACKEND_URL + "/api/register",
				{
				  method: "POST",
				  headers: {
					"Content-Type": "application/json",
				  },
				  body: JSON.stringify({ email, password }),
				}
			  );
			  if (!response.ok) {
				return false;
			  }
			  const data = await response.json();
			  // Guarda el token en localStorage
			  localStorage.setItem("token", data.token);
			  return true;
			} catch (error) {
			  console.log(error);
			}
		  },

		login: async (email, password) => {
		  try {
			const response = await fetch(
			  process.env.BACKEND_URL + "/api/signin",
			  {
				method: "POST",
				headers: {
				  "Content-Type": "application/json",
				},
				body: JSON.stringify({ email, password }),
			  }
			);
			if (!response.ok) {
			  return false;
			}
			const data = await response.json();
			localStorage.setItem("token", data.token);
			return true;
		  } catch (error) {
			console.log(error);
		  }
		},
	  },
	};
  };
  
  export default getState;