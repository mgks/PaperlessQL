import core from './core/core.js';
import pql_config from './config.js';

const schema = {
    data: {
      id: Number,
      data: String,
    },
    temp_data: {
      id: Number,
      name: String,
    },
  };

 // Define the PQL commands
 const commands = {
    SELECT: function(tableName, filterFunction) {
      let table = JSON.parse(localStorage.getItem(tableName));
      if (filterFunction) {
        table = table.filter(filterFunction);
      }
      return table;
    },
    INSERT: function(tableName, data) {
      let table = JSON.parse(localStorage.getItem(tableName));
      if (!table) {
        table = [];
      }
      table.push(data);
      localStorage.setItem(tableName, JSON.stringify(table));
    },
    DELETE: function(tableName, filterFunction) {
      let table = JSON.parse(localStorage.getItem(tableName));
      table = table.filter((row) => !filterFunction(row));
      localStorage.setItem(tableName, JSON.stringify(table));
    },
    UPDATE: function(tableName, filterFunction, updateFunction) {
      let table = JSON.parse(localStorage.getItem(tableName));
      table = table.map((row) => {
        if (filterFunction(row)) {
          return updateFunction(row);
        }
        return row;
      });
      localStorage.setItem(tableName, JSON.stringify(table));
    },
  };
  
  // Define the PQL interface
  const PQL = {
    check: function(data){
        return check_scheme(data);
    },
    select: function(tableName, filterFunction) {
      return commands.SELECT(tableName, filterFunction);
    },
    insert: function(tableName, data) {
      return commands.INSERT(tableName, data);
    },
    delete: function(tableName, filterFunction) {
      return commands.DELETE(tableName, filterFunction);
    },
    update: function(tableName, filterFunction, updateFunction) {
      return commands.UPDATE(tableName, filterFunction, updateFunction);
    },
  };
  
  // Example usage
  PQL.insert("users", { id: 1, name: "John Doe", email: "john.doe@example.com" });
  PQL.insert("users", { id: 2, name: "Jane Doe", email: "jane.doe@example.com" });
  
  const users = PQL.select("users", (user) => user.id === 1);
  console.log(users);
  
  PQL.update("users", (user) => user.id === 1, (user) => ({ ...user, name: "New Name" }));
  
  PQL.delete("users", (user) => user.id === 2);
  

  /// test area
  PQL.check();

