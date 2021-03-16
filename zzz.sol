contract Test
{
    enum RequestType{NewHome, EditHome}
    
    struct Ownership
    {
        string homeAddress;
        address owner;
        uint p;
    }   
    
    struct Owner{
        string name;
        uint passSer;
        uint passNum;
        uint256 date;
        string phoneNumber;
    }
    
    struct Home
    {
        string homeAddress;
        uint area;
        uint cost;
    }
    struct Request
    {
        RequestType requestType;
        Home home;
        uint result;
        address adr;
    }
    struct Employee
    {
        string nameEmployee;
        string position;
        string phoneNumber;
    }
    
    mapping(string => Employee) private employees;
    mapping(address => Owner) private owners;
    mapping(address => Request) private requests;
    mapping(string => Home) private homes;
    mapping(string => Ownership[]) private ownerships;
    
    function AddHome(string memory _adr, uint _area, uint _cost) public {
        Home memory h;
        h.homeAddress = _adr;
        h.area = _area;
        h.cost = _cost;
        homes[_adr] = h;
    }
    function GetHome(string memory adr) public returns (uint _area, uint _cost){
        return (homes[adr].area, homes[adr].cost);
    }
    function AddEmployee(string memory _name, string memory _pos, string memory _phone) public{
        Employee memory e;
        e.nameEmployee = _name;
        e.position = _pos;
        e.phoneNumber = _phone;
        employees[_name] = e;
    }
    function GetEmployee(string memory name) public returns (string memory _pos, string memory _phone) {
        return (employees[name].position, employees[name].phoneNumber);
    }
    function EditEmployee(string memory name, string memory newPos, string memory newPhone) public
    {
        employees[name].position = newPos;
        employees[name].phoneNumber = newPhone;
    }
}
