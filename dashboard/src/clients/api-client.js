
function client(
  endpoint,
  {body, ...customConfig} = {},
) {

  const config = {
    method: body ? "POST" : "GET",
    body: body ? JSON.stringify(body) : undefined,
    headers: {
      "Content-Type": body ? "application/json" : undefined,
      ...customConfig.headers,
    },
    ...customConfig,
  };

  return fetch(`${process.env.REACT_APP_RSS_API_URL}/${endpoint}`, config)
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        const errorMessage = response.text();
        return Promise.reject(new Error(errorMessage));
      }
    });
}

export {client}