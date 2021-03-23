contract Owned
{
    address private owner;
    
    constructor() public
    {
        owner = msg.sender;
    }
    
    modifier OnlyOwner
    {
        require
        (
            msg.sender == owner,
            'Only owner can run this function!'
        );
        _;
    }
    
    function ChangeOwner(address newOwner) public OnlyOwner
    {
        owner = newOwner;
    }
    
    function GetOwner() public returns (address)
    {
        return owner;
    }
}

contract Test is Owned
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
    }
    struct Employee
    {
        string nameEmployee;
        string position;
        string phoneNumber;
        bool isset;
    }
    
    modifier OnlyEmployee
    {
        require
        (
            employees[msg.sender].isset != false,
            'Only Employee can run this function'
        );
        _;
    }
    
    mapping(address => Employee) private employees;
    mapping(address => Owner) private owners;
    mapping(address => Request) private requests;
    mapping(string => Home) private homes;
    mapping(string => Ownership[]) private ownerships;
    mapping(uint => address) private reqAdr;
    uint id = 0;
    
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
    function AddEmployee(address _adr, string memory _name, string memory _pos, string memory _phone) public OnlyOwner {
        Employee memory e;
        e.nameEmployee = _name;
        e.position = _pos;
        e.phoneNumber = _phone;
        e.isset = true;
        employees[_adr] = e;
    }
    function GetEmployee(address adr) public OnlyOwner returns (string memory _name, string memory _pos, string memory _phone) {
        return (employees[adr].nameEmployee, employees[adr].position, employees[adr].phoneNumber);
    }
    function EditEmployee(address _adr, string memory _name, string memory _pos, string memory _phone) public OnlyOwner
    {
        employees[_adr].nameEmployee = _name;
        employees[_adr].position = _pos;
        employees[_adr].phoneNumber = _phone;
    }
     function DeleteEmployee(address _adr) public OnlyOwner
    {
        delete employees[_adr];
    }
    function AddRequestForNewHome(address _adr, string memory _homeAddress) public {
        Request memory r;
        r.requestType = RequestType.NewHome;
        r.home = homes[_homeAddress];
        requests[_adr] = r;
        reqAdr[id] = _adr;
        id = id + 1;
    }
    function GetRequests() public returns (string[] memory, uint[] memory, uint[] memory) {
        string[] memory adr = new string[](id);
        uint[] memory area = new uint[](id);
        uint[] memory cost = new uint[](id);
        for (uint i = 0; i < id; i++) {
            adr[i] = requests[reqAdr[i]].home.homeAddress;
            area[i] = requests[reqAdr[i]].home.area;
            cost[i] = requests[reqAdr[i]].home.cost;
        }
        return (adr, area, cost);
    }
}
