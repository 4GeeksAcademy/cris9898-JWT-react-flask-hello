const getState = ({ getStore, getActions, setStore }) => {
	return {
	  store: {
		users: []
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
			
			  localStorage.setItem("token", data.token);
			  return true;
			} catch (error) {
			  console.log(error);
			}
		  },

		  login: async (email, password) => {
			try {
				const response = await fetch(
					`${process.env.BACKEND_URL}/api/login`, 
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
				console.error("Login failed:", error);
				return false;
			}
		},

		getUsers: async () => {
			const store = getStore();

			try {
				const response = await fetch(`${process.env.BACKEND_URL}/api/users`)
				if (!response.ok) {
					throw new error("No se cargo la API");
				}
				const data = await response.json();
				console.log(data);


				setStore({ users: data });


			} catch (error) {
				console.log("Entro en el catch del getUsers:")
				console.log(error)
			}
		},
	  },
	};
  };
  
  export default getState;